use std::error::Error;
use std::io::{Read, Write};
use dds::{ColorFormat, Encoder, Format, ImageView, Size};
use dds::header::Header;
use itertools::Itertools;

#[derive(Debug)]
pub struct Pixel {
    pub r: f32,
    pub g: f32,
    pub b: f32,
    pub a: f32
}

impl Pixel {
    pub fn to_be_bytes(&self) -> [u8; 16] {
        [
            self.r.to_be_bytes(),
            self.g.to_be_bytes(),
            self.b.to_be_bytes(),
            self.a.to_be_bytes()
        ].concat().into_iter()
            .collect_array::<16>().expect("16 bytes")
    }

    pub fn to_le_bytes(&self) -> [u8; 16] {
        [
            self.r.to_le_bytes(),
            self.g.to_le_bytes(),
            self.b.to_le_bytes(),
            self.a.to_le_bytes()
        ].concat().into_iter()
            .collect_array::<16>().expect("16 bytes")
    }
    
    pub fn from_le_bytes(data: &[u8; 16]) -> Self {
        let vals = data.chunks_exact(4)
            .map(|chunk| {
                f32::from_le_bytes(chunk.try_into().unwrap())
            })
            .collect::<Vec<_>>();

        Pixel {
            r: vals[0],
            g: vals[1],
            b: vals[2],
            a: vals[3]
        }
    }
    
    pub fn from_be_bytes(data: &[u8; 16]) -> Self {
        let vals = data.chunks_exact(4)
            .map(|chunk| {
                f32::from_be_bytes(chunk.try_into().unwrap())
            })
            .collect::<Vec<_>>();

        Pixel {
            r: vals[0],
            g: vals[1],
            b: vals[2],
            a: vals[3]
        }
    }
}

pub struct BasicDDSImage {
    pub width: u32,
    pub height: u32,
    pub pixels: Vec<Pixel>
}

impl BasicDDSImage {
    pub fn to_be_bytes(&self) -> Vec<u8> {
        let mut output = Vec::with_capacity(self.pixels.len()*16+2*4);

        output.extend_from_slice(&self.width.to_be_bytes());
        output.extend_from_slice(&self.height.to_be_bytes());
        for pixel in &self.pixels {
            output.extend_from_slice(&pixel.to_be_bytes());
        }

        output
    }

    pub fn pixel_bytes_le(&self) -> Vec<u8> {
        let mut output = Vec::with_capacity(self.pixels.len()*16);
        for pixel in &self.pixels {
            output.extend_from_slice(&pixel.to_le_bytes());
        }

        output
    }

    pub fn from_byte_stream(mut stream: impl Read) -> Result<Self, Box<dyn Error>> {
        let mut buffer = [0_u8; 4];

        stream.read_exact(&mut buffer)?;
        let width = u32::from_be_bytes(buffer);
        stream.read_exact(&mut buffer)?;
        let height = u32::from_be_bytes(buffer);

        //eprintln!("width: {}, height: {}", width, height);

        let Some(num_pixels) = width.checked_mul(height) else {
            return Err(format!("image with dims {width}x{height} is too large to represent in memory").into())
        };
        let mut pixels = Vec::<Pixel>::with_capacity(num_pixels as usize);
        let mut pixel_buffer = [0_u8; 4*4];
        for _ in 0..num_pixels {
            stream.read_exact(&mut pixel_buffer)?;
            let pixel = Pixel::from_be_bytes(&pixel_buffer);
            //eprintln!("{:?}", pixel);
            pixels.push(pixel);
        }

        Ok(Self {
            width,
            height,
            pixels
        })
    }

    pub fn from_dds_stream(stream: impl Read) -> Result<Self, Box<dyn Error>> {
        let mut decoder = dds::Decoder::new(stream)?;
        decoder.format().color();
        // ensure the file contains a single texture
        if !decoder.layout().is_texture() {
            return Err("Layout is not single texture; Probably not an LUT!".into())
        }
        // prepare a buffer to decode as 8-bit RGBA
        let size = decoder.main_size();
        let mut data = vec![0_u8; size.pixels() as usize * 4 * 4];
        let Some(view) = dds::ImageViewMut::new(&mut data, size, dds::ColorFormat::RGBA_F32) else {
            return Err("Failed to create image view".into())
        };
        // decode into the buffer
        decoder.read_surface(view)?;

        let pixels = data
            .chunks_exact(4*4)
            .map(|chunk| {
                Pixel::from_le_bytes(&chunk.try_into().expect("16 bytes"))
            })
            .collect();

        let width = size.width;
        let height = size.height;

        //let pixels = pixels.collect::<Vec<_>>();

        //eprintln!("Size: {x}x{y}");

        Ok(Self {
            width,
            height,
            pixels
        })
    }

    pub fn write_dds_to_stream(&self, writer: impl Write) -> Result<(), Box<dyn Error>> {
        let format = Format::R32G32B32A32_FLOAT;
        let Some(header) = Header::new_image(self.width, self.height, format).to_dx10() else {
            return Err("Failed to create header as dx10.".into())
        };

        let mut encoder = Encoder::new(writer, format, &Header::Dx10(header))?;

        let pixel_data = self.pixel_bytes_le();
        let Some(view) = ImageView::new(&pixel_data, Size::new(self.width, self.height), ColorFormat::RGBA_F32) else {
            return Err("Invalid image data".into());
        };

        encoder.write_surface(view)?;
        encoder.is_done();
        encoder.finish()?;
        Ok(())
    }
}