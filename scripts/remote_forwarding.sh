#!/bin/bash
ssh -N -R 2222:localhost:5000 -i EmbeddedSystems_key.pem danielcrovo@20.169.163.218
