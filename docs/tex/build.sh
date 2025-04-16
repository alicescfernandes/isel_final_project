rm -rf build
mkdir -p build
chmod u+w build
pdflatex --interaction=nonstopmode -output-directory=build 00_PRJ_main.tex
cd build && makeglossaries 00_PRJ_main
cd ..
pdflatex --interaction=nonstopmode -output-directory=build 00_PRJ_main.tex

mv build/00_PRJ_main.pdf final_report.pdf