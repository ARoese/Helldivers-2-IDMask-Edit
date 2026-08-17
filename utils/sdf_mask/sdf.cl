
bool inside_shape(
    __read_only const image2d_t binary_image,
    uint2 coordinate
) {
    float4 pix = read_imagef(binary_image, convert_int2(coordinate));
    float sample = (pix.x + pix.y + pix.z) / 3;
    return sample > 0.5;
}

uint2 dim2d(__read_only const image2d_t binary_image) {
    return (uint2)(get_image_width(binary_image), get_image_height(binary_image));
}

bool within_bounds(int2 coord, uint2 bounds) {
    return coord.x > 0 && coord.y > 0 && coord.x < bounds.x && coord.y < bounds.y;
}

float distance(int2 coord) {
    return sqrt((float)coord.x*coord.x + (float)coord.y*coord.y);
}

float distance_to_bound(
    __read_only const image2d_t binary_image,
    uint2 coordinate,
    uint max_distance
) {
    bool am_inside = inside_shape(binary_image,coordinate);
    uint2 dim = dim2d(binary_image);

    float current_distance = (float)max_distance;
    for(int x = 0; x <= max_distance*2; x++) {
        for(int y = 0; y <= max_distance*2; y++) {
            int2 target = (int2)(coordinate.x - max_distance + x, coordinate.y - max_distance + y);
            float dist = distance(convert_int2(coordinate) - target);
            bool target_in_shape = inside_shape(binary_image, convert_uint(target));
            bool target_is_opposite = am_inside ^ target_in_shape;
            if(within_bounds(target, dim) && target_is_opposite ){
                // this implicitly checks dist < max_distance because we start at max_distance
                current_distance = min(current_distance, dist);
            }
        }
    }

    // we want boundary pixels to equal 0.5, with inner pixels being higher
    // and outer pixel being lower
    float distance_ratio = current_distance / (max_distance*2);
    if (am_inside) {
        return 0.5 + distance_ratio;
    } else {
        return 0.5 - distance_ratio;
    }
    
}

__kernel void sdf(
    __read_only const image2d_t binary_image,
    __write_only image2d_t sdf_image,
    uint spread_pixels
) {
    uint2 pix_coord = (uint2)(get_global_id(0), get_global_id(1));
    uint2 image_dim = dim2d(binary_image);
    //write_imagef(sdf_image, convert_int2(pix_coord), 0.5);
    if (!within_bounds(convert_int2(pix_coord), image_dim)) {
        return;
    }

    float d2b = distance_to_bound(binary_image, pix_coord, (float)spread_pixels);
    write_imagef(sdf_image, convert_int2(pix_coord), d2b);
    
}