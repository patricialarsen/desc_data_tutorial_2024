import fnmatch
import numpy as np

def select_subset(available, wanted=None):
    if wanted is None:
        available_default = None
        if isinstance(available, dict):
            available_default = [k for k, v in available.items() if v.get('included_by_default') or v.get('include_in_default_catalog_list')]
        return set(available_default) if available_default else set(available)
        
    wanted = set(wanted)
    output = set()

    for item in wanted:
        matched = fnmatch.filter(available, item)
        if not matched:
            raise KeyError("{} does not match any available names: {}".format(item, ', '.join(sorted(available))))
        output.update(matched)

    return tuple(sorted(output))


def interpret_result(test_result):
    print("Status code:")
    print(test_result.status_code)
    print()
    if test_result.inspect_only:
        print("No pass/fail criterion specified, inspection only")
    elif test_result.passed:
        print("Test passed!")
    else:
        print("Test failed!")
    print()
    print("Summary message:")
    print(test_result.summary)
    return 


def trace(ixx,ixy,iyy):
    return (ixx+iyy)

def e(ixx,ixy,iyy):
    ixx = np.complex128(ixx)
    ixy = np.complex128(ixy)
    iyy = np.complex128(iyy)
    denom = (ixx+iyy + 2.*np.sqrt(ixx*iyy-ixy**2))
    e = (ixx-iyy+2*ixy*1j)/denom
    return e

# borrowed from GCRCatalogs
def convert_nanoJansky_to_mag(flux):
    """Convert calibrated nanoJansky flux to AB mag.
    """
    AB_mag_zp_wrt_Jansky = 8.90  # Definition of AB
    # 9 is from nano=10**(-9)
    AB_mag_zp_wrt_nanoJansky = 2.5 * 9 + AB_mag_zp_wrt_Jansky

    return -2.5 * np.log10(flux) + AB_mag_zp_wrt_nanoJansky