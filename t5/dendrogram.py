import matplotlib.pyplot as plt

def visit_cluster(tree, labels, xticks, counter = 0):
    if isinstance(tree[0], tuple):
        (blx, bly) = visit_cluster(tree[0], labels, xticks)
    else:
        (blx, bly) = (0, len(labels))
        labels.append(tree[0])
    if isinstance(tree[1], tuple):
        (brx, bry) = visit_cluster(tree[1], labels, xticks)
    else:
        (brx, bry) = (0, len(labels))
        labels.append(tree[1])

    (ulx, uly) = (tree[2], bly)
    (urx, ury) = (tree[2], bry)

    plt.plot([blx, ulx, urx, brx], [bly, uly, ury, bry], "k")

    xticks.append(tree[2])

    return (tree[2], (bly + bry) / 2)

# tree = (((A, B, dist), C, dist), ...)
def plot(tree):
    labels = []
    xticks = [0]
    
    visit_cluster(tree, labels, xticks)

    plt.yticks(list(range(len(labels))), labels)
    plt.xlim(0, max(xticks) + 1)
    plt.xticks(xticks)

    plt.show()