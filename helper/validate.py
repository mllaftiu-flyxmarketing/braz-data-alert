import os
import platform
from configs.globals import memory_limit
try:
    import resource
except Exception:
    resource = None

def validate_monthly_fields(result: list):
    for row in result:
        # Ensure month_field is in correct format
        if 'month_field' in row and isinstance(row['month_field'], str) and len(row['month_field']) == 7:
            row['month_field'] = f"{row['month_field']}-01"
        
        # Validate and convert numeric fields
        numeric_fields = [
            'clicks', 'unique_clicks', 'shows', 'unique_shows', 'registrations',
            'first_depositors', 'first_deposits', 'fd_sum_of_deposits', 'fd_number_of_deposits',
            'number_of_deposits', 'payments', 'payouts', 'bets', 'wins', 'bonuses',
            'payments_commissions', 'payouts_commissions', 'admin_fee', 'chargebacks',
            'royalty', 'cpa_amount', 'partner_profit', 'program_profit', 'total_profit',
            'number_of_depositors', 'ggr', 'click2reg', 'reg2dep', 'ngr'
        ]
        
        for field in numeric_fields:
            if field in row:
                try:
                    # Convert to float first to handle both string and numeric inputs
                    value = float(row[field]) if row[field] is not None else 0.0
                    # Round to 2 decimal places for monetary values
                    if field in ['payments', 'payouts', 'bets', 'wins', 'bonuses', 
                               'payments_commissions', 'payouts_commissions', 'admin_fee',
                               'chargebacks', 'royalty', 'cpa_amount', 'partner_profit',
                               'program_profit', 'total_profit', 'ggr', 'ngr']:
                        value = round(value, 2)
                    # Ensure click2reg and reg2dep are within reasonable bounds (0-100)
                    elif field in ['click2reg', 'reg2dep']:
                        value = max(0, min(100, float(value) if value else 0))
                    row[field] = value
                except (ValueError, TypeError):
                    row[field] = 0.0  # Default to 0 if conversion fails
    
    return result


def validate_daily_fields(result: list):
    for row in result:
        # Validate and convert numeric fields
        numeric_fields = [
            'clicks', 'unique_clicks', 'shows', 'unique_shows', 'registrations',
            'first_depositors', 'first_deposits', 'fd_sum_of_deposits', 'fd_number_of_deposits',
            'number_of_deposits', 'payments', 'payouts', 'bets', 'wins', 'bonuses',
            'payments_commissions', 'payouts_commissions', 'admin_fee', 'chargebacks',
            'royalty', 'cpa_amount', 'partner_profit', 'program_profit', 'total_profit',
            'number_of_depositors', 'ggr', 'click2reg', 'reg2dep', 'ngr'
        ]
        
        for field in numeric_fields:
            if field in row:
                try:
                    # Convert to float first to handle both string and numeric inputs
                    value = float(row[field]) if row[field] is not None else 0.0
                    # Round to 2 decimal places for monetary values
                    if field in ['payments', 'payouts', 'bets', 'wins', 'bonuses', 
                               'payments_commissions', 'payouts_commissions', 'admin_fee',
                               'chargebacks', 'royalty', 'cpa_amount', 'partner_profit',
                               'program_profit', 'total_profit', 'ggr', 'ngr']:
                        value = round(value, 2)
                    # Ensure click2reg and reg2dep are within reasonable bounds (0-100)
                    elif field in ['click2reg', 'reg2dep']:
                        value = max(0, min(100, float(value) if value else 0))
                    row[field] = value
                except (ValueError, TypeError):
                    row[field] = 0.0  # Default to 0 if conversion fails
    
    return result

def create_file_if_not_exists(directory: str, file_name: str):
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("")

def create_dir_if_not_exists(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def set_memory_limit():
    SET_GB = int(memory_limit) * 1024 * 1024 * 1024
    if platform.system() == "Windows":
        import ctypes
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x100
        JobObjectExtendedLimitInformation = 9

        class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", ctypes.c_uint32),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", ctypes.c_uint32),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", ctypes.c_uint32),
                ("SchedulingClass", ctypes.c_uint32),
            ]

        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [
                ("ReadOperationCount", ctypes.c_ulonglong),
                ("WriteOperationCount", ctypes.c_ulonglong),
                ("OtherOperationCount", ctypes.c_ulonglong),
                ("ReadTransferCount", ctypes.c_ulonglong),
                ("WriteTransferCount", ctypes.c_ulonglong),
                ("OtherTransferCount", ctypes.c_ulonglong),
            ]

        class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
                ("IoInfo", IO_COUNTERS),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]

        hJob = kernel32.CreateJobObjectW(None, None)
        if hJob:
            info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
            info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_PROCESS_MEMORY
            info.ProcessMemoryLimit = SET_GB
            kernel32.SetInformationJobObject(
                hJob,
                JobObjectExtendedLimitInformation,
                ctypes.byref(info),
                ctypes.sizeof(info),
            )
            kernel32.AssignProcessToJobObject(hJob, kernel32.GetCurrentProcess())
        return
    if resource is None:
        return
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    if hard == getattr(resource, "RLIM_INFINITY", -1):
        resource.setrlimit(resource.RLIMIT_AS, (SET_GB, SET_GB))
    else:
        new_soft = SET_GB if SET_GB <= hard else hard
        resource.setrlimit(resource.RLIMIT_AS, (new_soft, hard))