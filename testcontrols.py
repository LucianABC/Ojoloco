import pygame

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No se detectó ningún control arcade. Revisa el USB.")
    quit()

# Usar el primer control detectado
control = pygame.joystick.Joystick(0)
control.init()

print(f"Control detectado: {control.get_name()}")
print("Presiona botones o mueve la palanca para ver los índices...")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Detectar Botones
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"BOTÓN presionado: {event.button}")
            
        # Detectar Palanca (Ejes)
        if event.type == pygame.JOYAXISMOTION:
            if abs(event.value) > 0.5: # Filtro de sensibilidad
                print(f"EJE {event.axis} movido a {event.value}")

        # Detectar la palanca si se comporta como un HAT (común en kits arcade)
        if event.type == pygame.JOYHATMOTION:
            print(f"HAT (Palanca) movido a: {event.value}")

pygame.quit()

""" 
dmesg | tail -n 50
[   30.424581] Bluetooth: HCI device and connection manager initialized
[   30.424611] Bluetooth: HCI socket layer initialized
[   30.424626] Bluetooth: L2CAP socket layer initialized
[   30.424651] Bluetooth: SCO socket layer initialized
[   30.462249] Bluetooth: HCI UART driver ver 2.3
[   30.462291] Bluetooth: HCI UART protocol H4 registered
[   30.463006] Bluetooth: HCI UART protocol Three-wire (H5) registered
[   30.464579] hci_uart_bcm serial0-0: supply vbat not found, using dummy regulator
[   30.464950] hci_uart_bcm serial0-0: supply vddio not found, using dummy regulator
[   30.468168] Bluetooth: HCI UART protocol Broadcom registered
[   30.496739] Loaded X.509 cert 'benh@debian.org: 577e021cb980e0e820821ba7b54b4961b8b4fadf'
[   30.497698] Loaded X.509 cert 'romain.perier@gmail.com: 3abbc6ec146e09d1b6016ab9d6cf71dd233f0328'
[   30.498664] Loaded X.509 cert 'sforshee: 00b28ddf47aef9cea7'
[   30.503988] Loaded X.509 cert 'wens: 61c038651aabdcf94bd0ac7ff06c7248db18c600'
[   30.655595] input: DragonRise Inc.   Generic   USB  Joystick   as /devices/platform/soc/3f980000.usb/usb1/1-1/1-1:1.0/0003:0079:0006.0001/input/input2
[   30.662640] dragonrise 0003:0079:0006.0001: input,hidraw0: USB HID v1.10 Joystick [DragonRise Inc.   Generic   USB  Joystick  ] on usb-3f980000.usb-1/input0
[   30.824727] Bluetooth: hci0: BCM: chip id 94
[   30.825200] Bluetooth: hci0: BCM: features 0x2e
[   30.827865] Bluetooth: hci0: BCM43430A1
[   30.827911] Bluetooth: hci0: BCM43430A1 (001.002.009) build 0000
[   30.833396] Bluetooth: hci0: BCM43430A1 'brcm/BCM43430A1.raspberrypi,model-zero-2-w.hcd' Patch
[   30.974815] EXT4-fs error (device mmcblk0p2): ext4_validate_block_bitmap:423: comm ext4lazyinit: bg 127: bad block bitmap checksum
[   31.001075] brcmfmac: F1 signature read @0x18000000=0x1541a9a6
[   31.013469] EXT4-fs error (device mmcblk0p2): ext4_validate_block_bitmap:423: comm ext4lazyinit: bg 255: bad block bitmap checksum
[   31.062213] EXT4-fs error (device mmcblk0p2): ext4_validate_block_bitmap:423: comm ext4lazyinit: bg 383: bad block bitmap checksum
[   31.126694] EXT4-fs error (device mmcblk0p2): ext4_validate_block_bitmap:423: comm ext4lazyinit: bg 511: bad block bitmap checksum
[   31.168650] EXT4-fs error (device mmcblk0p2): ext4_validate_block_bitmap:423: comm ext4lazyinit: bg 639: bad block bitmap checksum
[   31.181955] brcmfmac: brcmf_fw_alloc_request: using brcm/brcmfmac43430-sdio for chip BCM43430/1
[   31.188083] usbcore: registered new interface driver brcmfmac
[   31.251624] EXT4-fs error (device mmcblk0p2): ext4_validate_block_bitmap:423: comm ext4lazyinit: bg 767: bad block bitmap checksum
[   31.283871] EXT4-fs error (device mmcblk0p2): ext4_validate_block_bitmap:423: comm ext4lazyinit: bg 880: bad block bitmap checksum
[   31.307346] EXT4-fs error (device mmcblk0p2): ext4_validate_block_bitmap:423: comm ext4lazyinit: bg 995: bad block bitmap checksum
[   31.546651] brcmfmac: brcmf_c_process_txcap_blob: no txcap_blob available (err=-2)
[   31.547313] brcmfmac: brcmf_c_preinit_dcmds: Firmware: BCM43430/1 wl0: Jun 14 2023 07:27:45 version 7.45.96.s1 (gf031a129) FWID 01-70bd2af7 es7
[   31.661023] Bluetooth: hci0: BCM: features 0x2e
[   31.662716] Bluetooth: hci0: BCM43436 37.4MHz Class 1.5 RaspBerry Pi Zero2 [Version: 1017.1042]
[   31.662757] Bluetooth: hci0: BCM43430A1 (001.002.009) build 1042
[   31.663438] Bluetooth: hci0: BCM: Using default device address (43:43:a1:12:1f:ac)
[   36.235191] Bluetooth: BNEP (Ethernet Emulation) ver 1.3
[   36.235233] Bluetooth: BNEP filters: protocol multicast
[   36.235266] Bluetooth: BNEP socket layer initialized
[   36.280976] Bluetooth: MGMT ver 1.23
[   36.315198] NET: Registered PF_ALG protocol family
[   36.943218] Bluetooth: RFCOMM TTY layer initialized
[   36.943293] Bluetooth: RFCOMM socket layer initialized
[   36.943340] Bluetooth: RFCOMM ver 1.11
[   41.417335] brcmfmac: brcmf_cfg80211_set_power_mgmt: power save enabled
[  577.026577] mmc1: Controller never released inhibit bit(s).
[  577.026841] brcmfmac: brcmf_sdio_read_control: read 2048 control bytes failed: -5
[  577.026869] brcmfmac: brcmf_sdio_rxfail: abort command, terminate frame, send NAK
 """