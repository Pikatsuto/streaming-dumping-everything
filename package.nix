{
  lib,
  python3Packages,
  fetchFromGitHub,
  fetchPypi,
  chromedriver,
  chromium,
  gnumake,
}:
############
# Packages #
#########################################################################
let
  comment = "Extract all content data for everything streaming site and download this";
  pname = "streaming-dumping-everything";
  version = "0.1";
in python3Packages.buildPythonApplication rec {
  ## ----------------------------------------------------------------- ##
  inherit pname version;
  doCheck = false;
  ## ----------------------------------------------------------------- ##
  src = ./.;
  ## ----------------------------------------------------------------- ##
  propagatedBuildInputs = let
    pythonPackages = with python3Packages; [
      setuptools
      wheel
    ];
    standardPackage = [
      chromedriver
      chromium
      gnumake
    ];
  in pythonPackages ++ standardPackage;
  ## ----------------------------------------------------------------- ##
  meta = with lib; {
    description = comment;
    homepage = "https://github.com/Pikatsuto/streaming-dumping-everything";
    license = licenses.gpl3;
    platforms = platforms.linux;
    maintainers = with maintainers; [ pikatsuto ];
    mainProgram = pname;
  };
  #######################################################################
}