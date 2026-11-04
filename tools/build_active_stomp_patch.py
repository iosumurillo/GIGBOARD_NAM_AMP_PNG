#!/usr/bin/env python3
"""
build_active_stomp_patch.py -- Generates byte-perfect (2735-byte compressed, 15288-byte uncompressed)
ActiveStomp.qml replacement for HeadRush firmware, replacing generic colored pedal blocks
with the authentic pedal artwork from ModuleEditors/img/<name>.png.
"""
import os
import sys
import zlib

def build_patched_qml(orig_qml: bytes) -> tuple[bytes, bytes]:
    # 1. Locate stompBody and Colorize block
    pos_body = orig_qml.find(b'id: stompBody')
    assert pos_body != -1, "stompBody not found"
    pos_start = orig_qml.rfind(b'Image {', 0, pos_body)
    pos_cached = orig_qml.find(b'cached: true', pos_body)
    pos_end = orig_qml.find(b'}', pos_cached) + 1

    old_block = orig_qml[pos_start:pos_end]

    # Realistic pedal artwork image replacement
    new_block = (
        b'Image {\n'
        b'\t\t\tid: stompBody\n'
        b'\t\t\tanchors.centerIn: parent\n'
        b'\t\t\twidth: 140\n'
        b'\t\t\theight: 220\n'
        b'\t\t\tfillMode: Image.PreserveAspectFit\n'
        b'\t\t\tsource: "../../Pages/ModuleEditors/img/" + signalChainModule.moduleTypeName.replace(" 2", "") + ".png"\n'
        b'\t\t\tvisible: true\n'
        b'\t\t}'
    )

    qml = orig_qml[:pos_start] + new_block + orig_qml[pos_end:]

    # 2. Hide generic text when realistic image is loaded
    old_text_vis = b'visible: !ampOrCab() && !signalChainModule.isIR'
    new_text_vis = b'visible: stompBody.status !== Image.Ready && !ampOrCab() && !signalChainModule.isIR'
    assert old_text_vis in qml, "old_text_vis not found"
    qml = qml.replace(old_text_vis, new_text_vis)

    # 3. Hide generic footswitch LED when realistic image is loaded
    old_led = (
        b'Image {\n'
        b'\t\t\tx: -15\n'
        b'\t\t\tsource: signalChainModule.active ? "../../img/FXModule_Active_5_StompSwitchLED.png" : "../../img/FXModule_Bypassed_3_StompSwitchLED.png"\n'
        b'\t\t}'
    )
    new_led = (
        b'Image {\n'
        b'\t\t\tx: -15\n'
        b'\t\t\tsource: signalChainModule.active ? "../../img/FXModule_Active_5_StompSwitchLED.png" : "../../img/FXModule_Bypassed_3_StompSwitchLED.png"\n'
        b'\t\t\tvisible: stompBody.status !== Image.Ready\n'
        b'\t\t}'
    )
    if old_led in qml:
        qml = qml.replace(old_led, new_led)

    # 4. Remove a long redundant comment to provide headroom
    comment = b'// signalChainModule.effectType == 1 ? 24 : 31 // MR was 34, but unless we have something to show "Stereo Doubler" correctly in the given rect, 31 is better than an odd word-wrap'
    if comment in qml:
        qml = qml.replace(comment, b'')

    target_uncomp = len(orig_qml)  # 15288
    target_comp = 2735

    print(f"Base modified QML length: {len(qml)} (target uncompressed: {target_uncomp})")
    assert len(qml) < target_uncomp, "Modified QML exceeds original uncompressed size"

    # Fast search for exact 2735 bytes compressed at level 9
    for n in range(1, 150):
        base_noise = [(i * 53 + 7) % 94 + 33 for i in range(n)]
        for char in range(33, 126):
            if char in (ord('*'), ord('/')):
                continue
            test_noise = bytearray(base_noise)
            test_noise[-1] = char
            noise_bytes = bytes([b for b in test_noise if b not in (ord('*'), ord('/'))])
            candidate = qml + b'/*' + noise_bytes + b'*/'
            diff = target_uncomp - len(candidate)
            if diff >= 0:
                candidate += b' ' * diff
                comp = zlib.compress(candidate, 9)
                if len(comp) == target_comp:
                    print(f"EXACT MATCH FOUND! noise_len={n}, char={chr(char)}, comp={len(comp)}, uncomp={len(candidate)}")
                    return candidate, comp

    # Varied position search
    for n in range(60, 130):
        base_noise = [(i * 53 + 7) % 94 + 33 for i in range(n)]
        for pos in range(0, min(n, 30), 2):
            for char in range(33, 126):
                if char in (ord('*'), ord('/')):
                    continue
                test_noise = bytearray(base_noise)
                test_noise[pos] = char
                noise_bytes = bytes([b for b in test_noise if b not in (ord('*'), ord('/'))])
                candidate = qml + b'/*' + noise_bytes + b'*/'
                diff = target_uncomp - len(candidate)
                if diff >= 0:
                    candidate += b' ' * diff
                    comp = zlib.compress(candidate, 9)
                    if len(comp) == target_comp:
                        print(f"EXACT MATCH FOUND! noise_len={n}, pos={pos}, char={chr(char)}, comp={len(comp)}, uncomp={len(candidate)}")
                        return candidate, comp

    raise RuntimeError("Could not find exact 2735-byte compression match")

if __name__ == "__main__":
    qml_path = "scratch/decompressed_qml/qml_025_1852310.qml"
    with open(qml_path, "rb") as f:
        orig_qml = f.read()

    patched_qml, comp_patch = build_patched_qml(orig_qml)
    with open("scratch/ActiveStomp_patched.qml", "wb") as f:
        f.write(patched_qml)
    with open("scratch/ActiveStomp_perfect_patch.bin", "wb") as f:
        f.write(comp_patch)

    print("Successfully generated:")
    print(f"  scratch/ActiveStomp_patched.qml ({len(patched_qml)} bytes)")
    print(f"  scratch/ActiveStomp_perfect_patch.bin ({len(comp_patch)} bytes)")
