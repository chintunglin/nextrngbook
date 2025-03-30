::: src.nextrngbook.dx_generator

!!! note "To ensure reproducibility for the RNG"    
    1. The `seed` should be provided with a fixed value (non-None).    
    2. The `dx32_id` should be fixed. Either use the default value or a specific 
    integer value (e.g., `270`).    
         
!!! danger "Caution" 
    If multiple `dx32_id` values exceeding the valid range are provided, 
    they might be mapped to the same internal `dx32_id`. This could lead to 
    the misconception that different, independent RNGs are being used, while 
    in fact they are the same. A warning will be issued to inform the user 
    about this mapping. Care should be taken when applying such mappings across 
    multiple threads or processes, 
    as they may introduce high correlations among results.
