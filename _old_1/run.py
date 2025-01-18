from gridclasses import DGrid, Grid
import pdb


def main():
    a1 = DGrid((3, 3))
    some_cell = a1.grid.get_cell((1, 1))
    some_object = some_cell.cell_objects[0]
    print("In level: ", a1.level)
    print("Some position: ", some_cell.position)
    print("Containing some object: ", some_object.name)

    print("Interpreter: ")
    pdb.set_trace()


if __name__ == "__main__":
    main()
