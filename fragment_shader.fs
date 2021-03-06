#version 330 core
in vec3 planeCoord;
out vec4 FragColor;

uniform sampler3D volumeTexture;
uniform vec3 cameraPos;
uniform mat4 camTransform;
uniform float delta;
uniform float stepSize;
uniform float tn;
uniform float tf;

void main()
{
    vec3 rayDirection = normalize(planeCoord- cameraPos);

    float c = 0.0;
    float accumulated_t = 0;

    for(float i = tn; i <= tf; i += stepSize){

        vec3 pos = cameraPos + rayDirection * i;

        vec3 queryPoint = (camTransform * vec4(pos.x, pos.y, pos.z, 1.0)).xyz;
        vec4 result = texture(volumeTexture, vec3(queryPoint.x + 0.5, queryPoint.y + 0.5, queryPoint.z + 0.5));

        float t = exp(-accumulated_t * delta);

        c += t * (1 - exp(-result.x * delta)); 
        accumulated_t += result.x;

    }

    FragColor = vec4(c, c, c, 1.0);

} 