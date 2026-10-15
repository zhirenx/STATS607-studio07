# Studio 07 - Robust Regression: Estimation and Prediction

Answer each scientific question in 2–4 sentences. Reference the figures you created to support your conclusions


## Figure A

OLS is the MLE under normal errors, while LAD is the MLE under Laplace errors. For normal errors, OLS consistently has a lower coefficient MSE than LAD. For Laplace errors, however, the LAD/OLS MSE ratio increases from 0.73 at p/n = 0.05 to 1.35 at p/n = 0.90, suggesting that LAD loses its advantage as dimensionality increases. Classical MLE efficiency results typically assume fixed p and large n, so they do not guarantee the same ranking in high-dimensional finite samples.


## Figure B

By looking at `figure_B.png`, it seems that both cases had similar performance in terms of the coefficient estimation quality, but LAD has worse prediction quality than OLS. Moreover, bad coefficient estimate does not seem to always correspond to bad prediction. For example, when `rho` is high (i.e. near 1), both LAD and OLS had high coeffieicnt MSE, indicating relatively bad coefficient estimation. However, the prediction MSE (which measures the goodness of prediction) for both cases remains stable compared to that under lower values of `rho`.
