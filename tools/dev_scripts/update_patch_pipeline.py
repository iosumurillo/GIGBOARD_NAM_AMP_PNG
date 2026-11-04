with open('core/patch_pipeline.c', 'rb') as f:
    c = f.read()

old1 = b'''  ElfPatchResult elf_result;
  if (!nam_elf_patch_gonkulator(evil_data, evil_len, tramp, target->engine_vtable_vaddr, target->orig_process_fn,
                                 &elf_result, err, err_size))'''

new1 = b'''  ElfPatchResult elf_result;
  if (!nam_elf_patch_gonkulator(evil_data, evil_len, tramp, target->engine_vtable_vaddr, target->orig_process_fn, 8u,
                                 &elf_result, err, err_size))'''

old2 = b'''  if (enable_v2_hijack)
  {
    if (!nam_elf_patch_gonkulator(evil_data, evil_len, tramp, target->v2_engine_vtable_vaddr,
                                   target->v2_orig_process_fn, &elf_result_v2, err, err_size))'''

new2 = b'''  if (enable_v2_hijack)
  {
    if (!nam_elf_patch_gonkulator(evil_data, evil_len, tramp, target->v2_engine_vtable_vaddr,
                                   target->v2_orig_process_fn, 8u, &elf_result_v2, err, err_size))'''

old3 = b'''  if (target->amp_engine_vtable_vaddr != 0 && target->amp_orig_process_fn != 0)
  {
    if (!nam_elf_patch_gonkulator(evil_data, evil_len, tramp, target->amp_engine_vtable_vaddr,
                                   target->amp_orig_process_fn, &elf_result_amp, err, err_size))'''

new3 = b'''  if (target->amp_engine_vtable_vaddr != 0 && target->amp_orig_process_fn != 0)
  {
    if (!nam_elf_patch_gonkulator(evil_data, evil_len, tramp, target->amp_engine_vtable_vaddr,
                                   target->amp_orig_process_fn,
                                   target->amp_process_slot ? target->amp_process_slot : 7u,
                                   &elf_result_amp, err, err_size))'''

if b'\r\n' in c:
    for pair in [(old1, new1), (old2, new2), (old3, new3)]:
        o = pair[0].replace(b'\n', b'\r\n')
        n = pair[1].replace(b'\n', b'\r\n')
        assert o in c, f"Could not find {o[:30]}"
        c = c.replace(o, n, 1)
else:
    for pair in [(old1, new1), (old2, new2), (old3, new3)]:
        assert pair[0] in c
        c = c.replace(pair[0], pair[1], 1)

with open('core/patch_pipeline.c', 'wb') as f:
    f.write(c)
print("Updated core/patch_pipeline.c successfully")

