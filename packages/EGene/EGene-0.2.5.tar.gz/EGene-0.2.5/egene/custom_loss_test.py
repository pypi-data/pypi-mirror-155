import egene


def loss_function(network):
    return abs(network.calico([2])[0])  # Should calico to 0


if __name__ == "__main__":
    spe = egene.Species([1, 3, 1], loss_function=loss_function)
    spe.train(50)
