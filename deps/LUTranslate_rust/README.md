# LUTranslate

translates LUT dds files to/from a simple non-jagged float matrix format.
This allows for much easier interop on the R32G32B32A32_FLOAT format that the LUT files
are often stored in. Most libraries cannot read or work with this format, so this acts
as the middleman between them.

Transfer format:
```
Pixel {
    r: float32_be
    g: float32_be
    b: float32_be
    a: float32_be
}

stdout {
    width: uint32_be
    height: uint32_be
    pixels: [width*height; Pixel]
}
```

## Building
For current OS:  
`cargo build --release`  
Cross-compile for windows:  
`cargo build --release --target x86_64-pc-windows-gnu`