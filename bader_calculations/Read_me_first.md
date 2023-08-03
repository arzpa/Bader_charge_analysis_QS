1) Run simple "scf" calculation for your structure.
2) Then do post processing using "pp.x" feature of QE. Remember that outdir and prefix name of your SCF and ppx bader calculation has to be the same!
   Use: pp.x < file.cube.in > file.cube.out (Use this in your batch.sh file)
3) The above command will give you "file.cube.xsf"  file which is used to get bader charges.
4) Run: bader -p all_atom file.cube.xsf (You have to run in it directly in the terminal)
