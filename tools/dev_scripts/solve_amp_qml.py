import zlib
import random
import re

with open('scratch/decompressed_qml/qml_025_1852310.qml', 'rb') as f:
    orig = f.read()

# 1. StompBody replacement for pedals (Anxiety OD etc.)
pos_body = orig.find(b'id: stompBody')
pos_start = orig.rfind(b'Image {', 0, pos_body)
pos_cached = orig.find(b'cached: true', pos_body)
pos_end = orig.find(b'}', pos_cached) + 1

new_block = (
    b'Image {\n'
    b'\tid: stompBody\n'
    b'\tanchors.centerIn: parent\n'
    b'\twidth: 140\n'
    b'\theight: 220\n'
    b'\tfillMode: Image.PreserveAspectFit\n'
    b'\tsource: signalChainModule.type > 0 && signalChainModule.typeProp && signalChainModule.typeProp.translator ? "qrc:/Pages/ModuleEditors/img/" + signalChainModule.typeProp.translator.string.replace(" 2", "") + ".png" : ""\n'
    b'\tvisible: status === Image.Ready\n'
    b'}'
)
qml = orig[:pos_start] + new_block + orig[pos_end:]

# 2. Hide text and led when image ready
qml = qml.replace(b'visible: !ampOrCab() && !signalChainModule.isIR',
                  b'visible: stompBody.status !== Image.Ready && !ampOrCab() && !signalChainModule.isIR')

old_led = (
    b'Image {\n'
    b'\t\t\tx: -15\n'
    b'\t\t\tsource: signalChainModule.active ? "../../img/FXModule_Active_5_StompSwitchLED.png" : "../../img/FXModule_Bypassed_3_StompSwitchLED.png"\n'
    b'\t\t}'
)
new_led = (
    b'Image {\n'
    b'\tx: -15\n'
    b'\tsource: signalChainModule.active ? "../../img/FXModule_Active_5_StompSwitchLED.png" : "../../img/FXModule_Bypassed_3_StompSwitchLED.png"\n'
    b'\tvisible: stompBody.status !== Image.Ready\n'
    b'}'
)
qml = qml.replace(old_led, new_led)

# 3. Fix Amp image source so "82 LEAD 800 (NAM)" maps back to "82 LEAD 800 Bright"
old_amp_src1 = b'source: "../../Pages/ModuleEditors/img/Amp/" + signalChainModule.subTypeAmpFinal + ".png"'
new_amp_src1 = b'source: "../../Pages/ModuleEditors/img/Amp/" + signalChainModule.subTypeAmpFinal.replace(" (NAM) ", " Bright") + ".png"'

old_amp_src2 = b'source: "../../Pages/ModuleEditors/img/Amp/" + signalChainModule.subTypeAmp2Final + ".png"'
new_amp_src2 = b'source: "../../Pages/ModuleEditors/img/Amp/" + signalChainModule.subTypeAmp2Final.replace(" (NAM) ", " Bright") + ".png"'

assert old_amp_src1 in qml, 'old_amp_src1 not found'
assert old_amp_src2 in qml, 'old_amp_src2 not found'

qml = qml.replace(old_amp_src1, new_amp_src1)
qml = qml.replace(old_amp_src2, new_amp_src2)

# Remove comments and reduce tabs
qml = re.sub(rb'//[^\n]*', b'', qml)
qml = re.sub(rb'\t\t+', b'\t', qml)

target_uncomp = 15288
target_comp = 2735

found = False
for seed in range(500):
    random.seed(seed)
    raw_pool = [random.randint(33, 126) for _ in range(800)]
    for n in range(150, 500):
        chars = bytes([b for b in raw_pool[:n] if b not in (ord('*'), ord('/'))])
        cand = qml + b'/*' + chars + b'*/'
        diff = target_uncomp - len(cand)
        if diff >= 0:
            cand += b' ' * diff
            comp = zlib.compress(cand, 9)
            if len(comp) == target_comp:
                print(f'SUCCESS! seed={seed}, n={n}, comp={len(comp)}, uncomp={len(cand)}')
                with open('core/active_stomp_patch.h', 'w') as out_h:
                    out_h.write('/* Auto-generated ActiveStomp artwork patch with Amp image mapping (2735 bytes) */\n')
                    out_h.write('#ifndef ACTIVE_STOMP_PATCH_H\n#define ACTIVE_STOMP_PATCH_H\n\n')
                    out_h.write('#include <stddef.h>\n#include <stdint.h>\n\n')
                    out_h.write('#define ACTIVE_STOMP_PATCH_LEN 2735\n\n')
                    out_h.write('static const uint8_t ACTIVE_STOMP_PATCH[ACTIVE_STOMP_PATCH_LEN] = {\n')
                    for i in range(0, len(comp), 16):
                        chunk = comp[i:i+16]
                        out_h.write('  ' + ','.join(f'0x{b:02x}' for b in chunk) + ',\n')
                    out_h.write('};\n\n#endif /* ACTIVE_STOMP_PATCH_H */\n')
                with open('scratch/ActiveStomp_patched.qml', 'wb') as f_out:
                    f_out.write(cand)
                found = True
                break
    if found:
        break

assert found, 'Could not find match'
print('Generated core/active_stomp_patch.h successfully!')

