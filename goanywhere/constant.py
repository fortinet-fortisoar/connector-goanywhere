""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

FILE_TRANSFER_MODULE = {
    "AS2": 1,
    "FTP": 2,
    "FTPS": 4,
    "SFTP": 8,
    "GoFast": 16,
    "GoDrive": 32,
    "Projects": 64,
    "Secure Folders": 128,
    "Secure Forms": 256,
    "Triggers": 512,
    "Secure Mail": 1024
}

DATE_RANGE = {
    "Today": 1,
    "Yesterday": 2,
    "Last 7 Days": 7,
    "Last 30 Days": 30,
    "Last 90 Days": 90,
    "Last 180 Days": 180,
    "Last 365 Days": 365,
}

GROUP_BY = {
    "Hour": 1,
    "Day Of Week": 2,
    "Day Of Month": 3,
    "Month": 4,
}

ACTIVE_SESSIONS_SERVICES = {
    "HTTPS Sessions": 1,
    "FTP Sessions": 2,
    "FTPS Sessions": 4,
    "SFTP Sessions": 8,
    "AS2 Sessions": 16,
    "GoFast Sessions": 32,
    "Agent Sessions": 64,
    "Admin Sessions": 128
}

JOBS_COMPLETED_STATUS = {
    "Success": 2,
    "Failed": 4,
    "Canceled": 8
}
