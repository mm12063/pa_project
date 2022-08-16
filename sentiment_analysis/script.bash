#!/bin/bash

cd all_data/ALB
mv fixed/*.csv ./
rmdir fixed
cd ../CBAK
mv fixed/*.csv ./
rmdir fixed
cd ../ENS
mv fixed/*.csv ./
rmdir fixed
cd ../LAC
mv fixed/*.csv ./
rmdir fixed
cd ../lithium
mv fixed/*.csv ./
rmdir fixed
cd ../SQM
mv fixed/*.csv ./
rmdir fixed
cd ../TIA
mv fixed/*.csv ./
rmdir fixed