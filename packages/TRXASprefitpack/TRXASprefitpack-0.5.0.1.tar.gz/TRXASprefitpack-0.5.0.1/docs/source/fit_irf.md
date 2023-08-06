# fit_irf

fit irf: fitting shape of instrumental response function
There are three irf shapes are avaliable.
1. gaussian 2. cauchy(lorenzian) 3. pseudo voigt shape
It uses lmfit python package to fit experimentally measured instrumental response function to three model irf shape.

```{Note}
* The number of time zero parameter should be same as the
  number of scan to fit.
* If you set shape of irf to pseudo voigt (pv), then
   you should provide two full width at half maximum
   value for gaussian and cauchy parts, respectively.
* This script is only useful when one can directly measure
   instrumental response function.
```


* usage: fit_irf.py 
                  [-h] [--irf {g,c,pv}] [--fwhm_G FWHM_G] [--fwhm_L FWHM_L]
                  [-t0 TIME_ZEROS [TIME_ZEROS ...]] [-t0f TIME_ZEROS_FILE]
                  [--slow] [-o OUT]
                  prefix

* positional arguments:
  * prefix                prefix for tscan files It will read prefix_i.txt

* optional arguments:
  * -h, --help            show this help message and exit
  * --irf {g,c,pv}        shape of instrument response function 
   1. g: gaussian distribution 
   2. c: cauchy distribution 
   3. pv: pseudo voigt profile, linear combination of gaussian distribution
      and cauchy distribution pv = eta*c+(1-eta)*g the mixing parameter is fixed according to Journal of
      Applied Crystallography. 33 (6): 1311–1316.
  * --fwhm_G FWHM_G       full width at half maximum for gaussian shape It
    should not used when you set cauchy irf function
  * --fwhm_L FWHM_L       full width at half maximum for cauchy shape It should
    not used when you did not set irf or use gaussian irf
    function
  * -t0 TIME_ZEROS [TIME_ZEROS ...], --time_zeros TIME_ZEROS [TIME_ZEROS ...]
    time zeros for each tscan
  * -t0f TIME_ZEROS_FILE, --time_zeros_file TIME_ZEROS_FILE
    filename for time zeros of each tscan
  * --slow                use slower but robust global optimization algorithm
  * -o OUT, --out OUT     prefix for output files

## Parameter bound scheme

* fwhm: temporal width of x-ray pulse
  * lower bound: 0.5*fwhm_init
  * upper bound: 2*fwhm_init

* t_0: centre or timezero for each scan
  * lower bound: t_0 - 2*fwhm_init
  * upper bound: t_0 + 2*fwhm_init

## Mixing parameter eta

For pseudo voigt IRF function, mixing parameter eta is guessed to

\begin{equation*}
\eta = 1.36603({fwhm}_L/f)-0.47719({fwhm}_L/f)^2+0.11116({fwhm}_L/f)^3
\end{equation*}

where
\begin{align*}
f &= ({fwhm}_G^5+2.69269{fwhm}_G^4{fwhm}_L+2.42843{fwhm}_G^3{fwhm}_L^2 \\
  &+ 4.47163{fwhm}_G^2{fwhm}_L^3+0.07842{fwhm}_G{fwhm}_L^4 \\
  &+ {fwhm}_L^5)^{1/5}
\end{align*}

This guess is according to [J. Appl. Cryst. (2000). **33**, 1311-1316](https://doi.org/10.1107/S0021889800010219)
