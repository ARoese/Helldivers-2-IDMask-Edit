// bool isn't actually standardized, so can't easily use it with pyopencl
#define bool int
#define true 1
#define false 0

bool inside_shape(
    __read_only const image2d_t binary_image,
    int2 coordinate
) {
    float4 pix = read_imagef(binary_image, convert_int2(coordinate));
    float sample = (pix.x + pix.y + pix.z) / 3;
    return sample >= 0.5;
}

int2 dim2d(__read_only const image2d_t binary_image) {
    return (int2)(get_image_width(binary_image), get_image_height(binary_image));
}

int2 dim2d_wo(__write_only const image2d_t binary_image) {
    return (int2)(get_image_width(binary_image), get_image_height(binary_image));
}

typedef struct {
    bool initialized;
    bool inside_shape;
    bool is_edge;
    int2 nearest_edge;
} SDFPixel;

// A dim.x by dim.y row-major 2d array of SDFPixel.
typedef struct {
    int2 dim;
    __global SDFPixel* pixels;
} SDFPixelArray;

// access flattened 2d array
__global SDFPixel* get_pixel(SDFPixelArray buffer, int2 coord) {
    return buffer.pixels + coord.x + coord.y * buffer.dim.x;
}

bool in_bounds(SDFPixelArray buffer, int2 coord) {
    return coord.x >= 0 && coord.y >= 0 && buffer.dim.x > coord.x && buffer.dim.y > coord.y;
}

// Uses the full laplacian edge detection kernel to determine if the given pixel coordinate is an edge pixel
// Kernel:
// [-1, -1, -1]
// [-1,  8, -1]
// [-1, -1, -1]
bool laplacian_edge_detect(__read_only const image2d_t binary_image, int2 location) {
    int2 image_dim = dim2d(binary_image);
    int sum = 0;
    // pixels on the edge of the image would need to sample off the side of the image to satisfy the kernel.
    // just say these pixels are not edges for our purposes
    if(location.x == 0 || location.x == image_dim.x-1 || location.y == 0 || location.y == image_dim.y-1 ) {
        return false;
    }

    // The kernel is small enough to write out each sample explicitly.
    // Start in the center, go up, then work clockwise around the kernel
    int2 test_loc = location;
    sum += inside_shape(binary_image, test_loc) ? 8 : 0;
    test_loc.y--;
    sum += inside_shape(binary_image, test_loc) ? -1 : 0;
    test_loc.x++;
    sum += inside_shape(binary_image, test_loc) ? -1 : 0;
    test_loc.y++;
    sum += inside_shape(binary_image, test_loc) ? -1 : 0;
    test_loc.y++;
    sum += inside_shape(binary_image, test_loc) ? -1 : 0;
    test_loc.x--;
    sum += inside_shape(binary_image, test_loc) ? -1 : 0;
    test_loc.x--;
    sum += inside_shape(binary_image, test_loc) ? -1 : 0;
    test_loc.y--;
    sum += inside_shape(binary_image, test_loc) ? -1 : 0;
    test_loc.y--;
    sum += inside_shape(binary_image, test_loc) ? -1 : 0;

    return sum > 0;
}

// Initialize SDFPixelArray buffer from the given binary image. It is assumed that
// the buffers passed to the other kernels have be initialized using this one 
__kernel void init(
    __read_only const image2d_t binary_image,
    __global SDFPixel* buffer
) {
    int2 pix_coord = (int2)((int)get_global_id(0), get_global_id(1));
    int2 image_dim = dim2d(binary_image);
    SDFPixelArray array = {
        .dim = image_dim,
        .pixels = buffer
    };
    
    if(in_bounds(array, pix_coord)) {
        __global SDFPixel* target_pix = get_pixel(array, pix_coord);
        target_pix->inside_shape = inside_shape(binary_image, pix_coord);
        bool is_edge = laplacian_edge_detect(binary_image, pix_coord);
        target_pix->initialized = is_edge;
        target_pix->is_edge = is_edge;
        target_pix->nearest_edge = is_edge ? pix_coord : (int2)(0,0);
    }
}

// distance between two pixels in pixel coordinates
int sq_dist(int2 a, int2 b) {
    int x = abs(a.x-b.x);
    int y = abs(a.y-b.y);
    return x*x+y*y;
}

// distance between two pixels in uv coordinates
float uv_sq_dist(int2 dim, int2 a, int2 b) {
    float x = abs(a.x-b.x)/(float)dim.x;
    float y = abs(a.y-b.y)/(float)dim.y;
    float distance = x*x+y*y;
    return distance;
}

/// Places the nearest edge to the given location from either a or or the pixel at coordinates b_coord into a.
/// if b_coord is out of bounds, does nothing and returns
void take_closest_to(int2 location, SDFPixelArray array, __global SDFPixel* a, int2 b_coord) {
    if(!in_bounds(array, b_coord)){
        return;
    }

    __global SDFPixel* b = get_pixel(array, b_coord);
    if(!b->initialized) {
        return; // can't get anything useful from here
    }else if(!a->initialized) {
        a->initialized = true;
        a->nearest_edge = b->nearest_edge; // take b, since it's the only one initialized
        return;
    }else if(uv_sq_dist(array.dim, location, a->nearest_edge) > uv_sq_dist(array.dim, location, b->nearest_edge)) {
        a->nearest_edge = b->nearest_edge;
    }
}

// run 1 pass of the JFA with the given jump distance. 
// expects that the buffer has been initialized by the init() kernel.
// This needs to be called on the same buffer multiple times with varying jump distances to complete the algorithm
__kernel void jfa_pass(
    int dim_x,
    int dim_y,
    int jump_dist,
    __global SDFPixel* buffer
) {
    int2 pix_coord = (int2)((int)get_global_id(0), get_global_id(1));
    SDFPixelArray array = {
        .dim = (int2)(dim_x, dim_y),
        .pixels = buffer
    };

    __global SDFPixel* target_pix = get_pixel(array, pix_coord);
    int2 test_coord = (int2)pix_coord;
    // upper left
    test_coord.x -= jump_dist;
    test_coord.y -= jump_dist;
    take_closest_to(pix_coord, array, target_pix, test_coord);
    // up
    test_coord.x += jump_dist;
    take_closest_to(pix_coord, array, target_pix, test_coord);
    // upper right
    test_coord.x += jump_dist;
    take_closest_to(pix_coord, array, target_pix, test_coord);
    // right
    test_coord.y += jump_dist;
    take_closest_to(pix_coord, array, target_pix, test_coord);
    // lower right
    test_coord.y += jump_dist;
    take_closest_to(pix_coord, array, target_pix, test_coord);
    // down
    test_coord.x -= jump_dist;
    take_closest_to(pix_coord, array, target_pix, test_coord);
    // lower left
    test_coord.x -= jump_dist;
    take_closest_to(pix_coord, array, target_pix, test_coord);
    // left
    test_coord.y -= jump_dist;
    take_closest_to(pix_coord, array, target_pix, test_coord);
}

// Convert a fully released buffer into an SDF
__kernel void generate_image(
    __write_only image2d_t sdf_image,
    __global SDFPixel* buffer,
    float max_distance
) {
    int2 pix_coord = (int2)((int)get_global_id(0), get_global_id(1));
    int2 image_dim = dim2d_wo(sdf_image);
    SDFPixelArray array = {
        .dim = image_dim,
        .pixels = buffer
    };

    __global SDFPixel* target_pix = get_pixel(array, pix_coord);
    // If the pixel is uninitialized, make it black
    float pix_val = 0.0;
    if(target_pix->initialized){ 
        float edge_distance = sqrt(uv_sq_dist(image_dim, pix_coord, target_pix->nearest_edge));

        // we want boundary pixels to equal 0.5, with inner pixels being higher
        // and outer pixel being lower
        float distance_ratio = edge_distance / (max_distance*2);
        float midpoint = 128.0 / 255.0;
        pix_val = target_pix->inside_shape ? midpoint + distance_ratio : midpoint - distance_ratio;
        pix_val = clamp(pix_val, 0.0f, 1.0f);
    }

    write_imagef(sdf_image, pix_coord, pix_val);
}