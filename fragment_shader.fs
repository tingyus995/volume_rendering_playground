#version 330 core
#define STEP_SIZE 0.01
#define DELTA 0.1
in vec3 planeCoord;
out vec4 FragColor;

uniform sampler3D volumeTexture;
uniform vec3 cameraPos;
uniform mat4 camTransform;

void main()
{
    mat4 mymat = mat4(1.0);
    vec3 rayDirection = normalize(planeCoord- cameraPos);

    float tn = 0.0f;
    float tf = 5.0f;

    vec3 rayBegin = cameraPos + rayDirection * tn;
    vec3 rayEnd = cameraPos + rayDirection * tf;

    float c = 0.0;
    float accumulated_t = 0;

    for(float i = tn; i <= tf; i += STEP_SIZE){

        vec3 pos = cameraPos + rayDirection * i;

        vec3 queryPoint = (camTransform * vec4(pos.x, pos.y, pos.z, 1.0)).xyz;
        vec4 result = texture(volumeTexture, vec3(queryPoint.x + 0.5, queryPoint.y + 0.5, queryPoint.z + 0.5));

        float t = exp(-accumulated_t * DELTA);

        c += t * (1 - exp(-result.x * DELTA)); 
        accumulated_t += result.x;

    }

    FragColor = vec4(c, c, c, 1.0);

} 