def load_file(filepath: str):
    """Loads a Wavefront OBJ file."""
    objects = {}
    vertices = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(filepath, "r"):  ## para cada linha do arquivo .obj
        if line.startswith("#"):
            continue

        values = line.split()  # quebra a linha por espaço
        if not values:
            continue

        ### recuperando vertices
        if values[0] == "v":
            vertices.append(values[1:4])

        ### recuperando coordenadas de textura
        elif values[0] == "vt":
            texture_coords.append(values[1:3])

        ### recuperando faces
        elif values[0] in ("usemtl", "usemat"):
            material = values[1]
        elif values[0] == "f":
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split("/")
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, material))

    model = {}
    model["vertices"] = vertices
    model["texture"] = texture_coords
    model["faces"] = faces

    return model


if __name__ == "__main__":
    model_file = input("Enter the name of the model file: ")
    model = load_file(model_file)
    print("Model: ", model)
