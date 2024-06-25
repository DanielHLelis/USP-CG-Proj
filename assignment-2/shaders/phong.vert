// vi: filetype=glsl
#version 410 core

in vec3 position;
in vec2 texture_coord;
in vec3 normal; // Add this input for normal data

out vec2 out_texture; // Changed from tex_coord to out_texture to match the fragment shader
out vec3 out_normal; // Output the normal to the fragment shader
out vec3 out_fragPos; // Output the fragment position to the fragment shader

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    vec4 worldPosition = model * vec4(position, 1.0); // Transform vertex to world coordinates
    gl_Position = projection * view * worldPosition; // Compute final position
    out_texture = texture_coord;
    out_normal = mat3(transpose(inverse(model))) * normal; // Correctly transform normals
    out_fragPos = vec3(worldPosition); // Pass world position to fragment shader
}
