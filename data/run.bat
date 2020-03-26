@echo off
echo **** Collecting Data ****
for /F "tokens=*" %%A in  (subs.txt) do python ..\dataTools\GenData.py -s %%A -c 10000 -o %%A.raw
echo ****  Cleaning Data  ****
for %%f in (*.raw) do python ..\dataTools\clean.py -i %%f -o %%~nf.clean
for %%f in (*.raw) do del %%f
echo ****  Combining Data   ****
copy *.clean data.comb
for %%f in (*.clean) do del %%f
echo ****  Processing Data  ****
python ..\dataTools\dupShuf.py -c 5 -i data.comb -o all.fin
del data.comb