#version 330 core
layout (location = 0) in vec2 aPos;

out vec3 planeCoord;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, 0.0, 1.0);
    planeCoord =  vec3(aPos.xy, -1);
}