# Copyright (c) 2022 NVIDIA CORPORATION.  All rights reserved.
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import numpy as np
import warp as wp

import math

wp.init()


@wp.kernel
def basic(x: wp.array(dtype=float)):
    
    tid = wp.tid()

    x[tid] = float(tid)*1.0


device = "cuda"
n = 32

x = wp.zeros(n, dtype=float, device="cuda")

wp.launch(
    kernel=basic, 
    dim=n, 
    inputs=[x], 
    device=device)

print(x.to("cpu").numpy())

# redefine kernel
@wp.kernel
def basic(x: wp.array(dtype=float)):
    
    tid = wp.tid()

    x[tid] = float(tid)*2.0
    

wp.launch(
    kernel=basic, 
    dim=n, 
    inputs=[x], 
    device=device)

print(x.to("cpu").numpy())