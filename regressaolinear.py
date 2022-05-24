def compute_mse(theta_0, theta_1, data):
    mse = 0
    counter = 0
    for _x_value, _y_value in data:
        hyp = theta_0 + (theta_1 * _x_value)
        mse = mse + ((hyp - _y_value) ** 2)
        counter += 1
    if counter:
        mse = mse/counter
    else:
        return 0
    return mse

def step_gradient(theta_0, theta_1, data, alpha):
    dX_0 = 0
    dX_1 = 0
    counter = 0
    for _x_value, _y_value in data:
        hyp = (theta_0 + (theta_1 * _x_value))
        dX_0 = dX_0 + (hyp - _y_value)
        dX_1 = dX_1 + (_x_value * (hyp - _y_value))
        counter += 1
    dX_0 = dX_0 * 2
    dX_1 = dX_1 * 2
    if counter:
        dX_0 = dX_0/counter
        dX_1 = dX_1/counter
    else:
        pass
    theta_0 = theta_0 - alpha * dX_0
    theta_1 = theta_1 - alpha * dX_1
    return theta_0, theta_1


def fit(data, theta_0, theta_1, alpha, num_iterations):
    th0_l = [theta_0]
    th1_l = [theta_1]
    for _i in range(num_iterations):
        theta_0, theta_1 = step_gradient(theta_0, theta_1, data, alpha)
        th0_l.append(theta_0)
        th1_l.append(theta_1)
    return th0_l, th1_l
