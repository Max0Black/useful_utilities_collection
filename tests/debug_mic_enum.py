import comtypes
from comtypes import CLSCTX_ALL, GUID, COMMETHOD, HRESULT, IUnknown
from ctypes import POINTER, c_void_p, cast
from ctypes.wintypes import BOOL, DWORD, LPWSTR, UINT

from comtypes.client import CreateObject


eRender = 0
eCapture = 1
eAll = 2

DEVICE_STATE_ACTIVE = 0x00000001

CLSID_MMDeviceEnumerator = GUID("{BCDE0395-E52F-467C-8E3D-C4579291692E}")
IID_IMMDeviceEnumerator = GUID("{A95664D2-9614-4F35-A746-DE8DB63617E6}")
IID_IMMDeviceCollection = GUID("{0BD7A1BE-7A1A-44DB-8397-C0A8CE878A5B}")
IID_IMMDevice = GUID("{D666063F-1587-4E43-81F1-B948E807363F}")
IID_IPropertyStore = GUID("{886d8eeb-8cf2-4446-8d02-cdba1dbdcf99}")

PKEY_Device_FriendlyName = (
    GUID("{A45C254E-DF1C-4EFD-8020-67D146A850E0}"),
    14,
)


class PROPERTYKEY(comtypes.Structure):
    _fields_ = [("fmtid", GUID), ("pid", DWORD)]


class PROPVARIANT(comtypes.Structure):
    _fields_ = [("vt", UINT), ("wReserved1", UINT), ("wReserved2", UINT), ("wReserved3", UINT), ("pszVal", LPWSTR)]


class IPropertyStore(IUnknown):
    _iid_ = IID_IPropertyStore
    _methods_ = [
        COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(DWORD), "cProps")),
        COMMETHOD([], HRESULT, "GetAt", (["in"], DWORD, "iProp"), (["out"], POINTER(PROPERTYKEY), "pkey")),
        COMMETHOD([], HRESULT, "GetValue", (["in"], POINTER(PROPERTYKEY), "key"), (["out"], POINTER(PROPVARIANT), "pv")),
    ]


class IMMDevice(IUnknown):
    _iid_ = IID_IMMDevice
    _methods_ = [
        COMMETHOD([], HRESULT, "Activate", (["in"], POINTER(GUID), "iid"), (["in"], DWORD, "dwClsCtx"), (["in"], c_void_p, "pActivationParams"), (["out"], POINTER(c_void_p), "ppInterface")),
        COMMETHOD([], HRESULT, "OpenPropertyStore", (["in"], DWORD, "stgmAccess"), (["out"], POINTER(POINTER(IPropertyStore)), "ppProperties")),
        COMMETHOD([], HRESULT, "GetId", (["out"], POINTER(LPWSTR), "ppstrId")),
        COMMETHOD([], HRESULT, "GetState", (["out"], POINTER(DWORD), "pdwState")),
    ]


class IMMDeviceCollection(IUnknown):
    _iid_ = IID_IMMDeviceCollection
    _methods_ = [
        COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(UINT), "pcDevices")),
        COMMETHOD([], HRESULT, "Item", (["in"], UINT, "nDevice"), (["out"], POINTER(POINTER(IMMDevice)), "ppDevice")),
    ]


class IMMDeviceEnumerator(IUnknown):
    _iid_ = IID_IMMDeviceEnumerator
    _methods_ = [
        COMMETHOD([], HRESULT, "EnumAudioEndpoints", (["in"], DWORD, "dataFlow"), (["in"], DWORD, "dwStateMask"), (["out"], POINTER(POINTER(IMMDeviceCollection)), "ppDevices")),
        COMMETHOD([], HRESULT, "GetDefaultAudioEndpoint", (["in"], DWORD, "dataFlow"), (["in"], DWORD, "role"), (["out"], POINTER(POINTER(IMMDevice)), "ppEndpoint")),
    ]


def get_friendly_name(device):
    store = device.OpenPropertyStore(0)
    key = PROPERTYKEY()
    key.fmtid = PKEY_Device_FriendlyName[0]
    key.pid = PKEY_Device_FriendlyName[1]
    value = store.GetValue(key)
    return value.pszVal


def get_id(device):
    return device.GetId()


def main():
    enumerator = CreateObject(CLSID_MMDeviceEnumerator, interface=IMMDeviceEnumerator)

    print("=== DEFAULT CAPTURE DEVICES ===")
    for role_name, role in [("Console", 0), ("Multimedia", 1), ("Communications", 2)]:
        try:
            dev = enumerator.GetDefaultAudioEndpoint(eCapture, role)
            print(f"{role_name}: {get_friendly_name(dev)} | {get_id(dev)}")
        except Exception as exc:
            print(f"{role_name}: ERROR -> {exc}")

    print("\n=== ALL ACTIVE CAPTURE DEVICES ===")
    collection = enumerator.EnumAudioEndpoints(eCapture, DEVICE_STATE_ACTIVE)
    count = collection.GetCount()
    print(f"Count: {count}")

    for i in range(count):
        try:
            dev = collection.Item(i)
            print(f"{i}: {get_friendly_name(dev)} | {get_id(dev)}")
        except Exception as exc:
            print(f"{i}: ERROR -> {exc}")


if __name__ == "__main__":
    main()