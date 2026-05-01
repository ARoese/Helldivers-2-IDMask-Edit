mod dds_image;

use std::error::Error;
use std::fs::{File, OpenOptions};
use std::io;
use std::io::{Read, Write};
use std::path::Path;
use crate::dds_image::BasicDDSImage;

use clap::Parser;
use clap::Args;

#[derive(Args, Debug)]
#[group(required = true, multiple = false)]
struct ConvertDirection {
    /// convert input to a dds file
    #[arg(long)]
    to_dds: bool,

    /// convert input to a matrix. Assumes input is a dds file
    #[arg(long)]
    from_dds: bool,
}

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Cli {
    /// Output file. Defaults to stdout if not given, or if '-' is passed
    #[arg(short, long)]
    out_path: Option<String>,

    /// Input file. Defaults to stdin if not given, or if '-' is passed
    #[arg(short, long)]
    in_path: Option<String>,

    #[command(flatten)]
    io: ConvertDirection
}

fn main() -> Result<(), Box<dyn Error>> {
    let test_dir = Path::new(env!("CARGO_MANIFEST_DIR")).join("test");;
    let test_file = test_dir.join("test_lut.dds");
    let copy_test = test_dir.join("test_lut_copy.dds");

    let args = Cli::parse();

    let source: Box<dyn Read> = match args.in_path.as_deref() {
        Some("-") | None => {
            Box::new(io::stdin().lock())
        },
        Some(path) => {
            let open_file = File::open(Path::new(path))?;
            Box::new(open_file)
        }
    };

    let mut dest: Box<dyn Write> = match args.out_path.as_deref() {
        Some("-") | None => {
            Box::new(io::stdout().lock())
        },
        Some(path) => {
            let open_file = OpenOptions::new()
                .write(true)
                .truncate(true)
                .create(true)
                .open(Path::new(path))?;
            Box::new(open_file)
        }
    };

    if args.io.to_dds {
        BasicDDSImage::from_byte_stream(source)?.write_dds_to_stream(dest)?;
    }else {
        let bytes = BasicDDSImage::from_dds_stream(source)?.to_be_bytes();
        dest.write_all(&bytes)?;
    };

    return Ok(());


    let file = File::open(test_file).expect("failed to open file");
    let image = BasicDDSImage::from_dds_stream(file).unwrap();
    println!("size: {}x{}", image.width, image.height);

    let out_file = File::create(copy_test).expect("failed to create file");
    image.write_dds_to_stream(out_file).unwrap();
}
