program alg
  use field_mod, only : r2d_field
  use kern_use_var_mod, only : kern_use_var
  use psy_alg, only : invoke_0_kern_use_var
  type(r2d_field) :: fld1

  call invoke_0_kern_use_var(fld1)

end program alg
