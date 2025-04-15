!!! danger "Caution"
    The `dx_generator` subpackage is 
    **not recommended for cryptographic applications**.  
    It is intended for statistical simulations or machine learning tasks only.

::: src.nextrngbook.dx_generator
    options:
        members: false
        show_root_heading: false
        show_source: false
        
---


### `create_dx(dx_id, seed)` 


!!! tip "Example `dx_id` values"
    | dx_id | k  | s | B      | p         | log₁₀(period) |
    |-------|-----|----|---------|------------|---------------|
    | 0     | 2   | 1  | 32693   | 2147483249 | 18.7          |
    | 556   | 3   | 2  | 32736   | 2147483579 | 28            |
    | 1030  | 5   | 1  | 32711   | 2147483497 | 46.7          |
    | 2000  | 8   | 1  | 32743   | 2147483269 | 74.7          |
    | 3000  | 13  | 2  | 32754   | 2147481143 | 121.3         |
    | 4000  | 1301| 2  | 1046381 | 2147472413 | 12140.8       |
    | 4194  | 50873| 2 | 1016882 | 2146123787 | 474729.3      |


::: src.nextrngbook.dx_generator.create_dx
    options:
        show_signature: true
        show_source: false
        show_root_heading: false


!!! note "To ensure reproducibility for the RNG"    
    1. The `seed` should be provided with a fixed value (non-None).    
    2. The `dx_id` should be fixed. Either use the default value or a specific 
    integer value (e.g., `270`).    
         
!!! danger "Caution" 
    If multiple `dx_id` values exceeding the valid range are provided, 
    they might be mapped to the same internal `dx_id`. This could lead to 
    the misconception that different, independent RNGs are being used, while 
    in fact they are the same. A warning will be issued to inform the user 
    about this mapping. Care should be taken when applying such mappings across 
    multiple threads or processes, 
    as they may introduce high correlations among results.


---

### `get_dx_max_id()`

::: src.nextrngbook.dx_generator.get_dx_max_id
    options:
        show_signature: true
        show_source: false
        show_root_heading: false

---

### `get_dx_id_table()`

::: src.nextrngbook.dx_generator.get_dx_id_table
    options:
        show_signature: true
        show_source: false
        show_root_heading: false

