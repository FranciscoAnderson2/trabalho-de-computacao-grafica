#version 330 core
out vec4 FragColor;

in vec2 TexCoord;
in vec3 Normal;
in vec3 FragPos;

uniform sampler2D textura;
uniform vec3 luzPos;
uniform vec3 cameraPos;

void main()
{

    vec4 corTex = texture(textura, TexCoord);

    if(corTex.a < 0.1)
        discard;

    vec3 n = normalize(Normal);              
    vec3 l = normalize(luzPos - FragPos);    
    vec3 v = normalize(cameraPos - FragPos); 

    vec3 r = reflect(-l, n);

    float ka = 0.55; 
    float kd = 0.9;  
    float ks = 0.8;  
    float e  = 16.0; 

    float La = 1.0;
    float Ld = 1.0;
    float Ls = 1.0;

    vec3 spotDir = normalize(vec3(0.0, 0.0, -1.0));

    float cutoff = cos(radians(65.0));

    float theta = dot(-l, spotDir);

    float I_ambiente = La * ka;

    float I_difusa   = 0.0;
    float I_especular = 0.0;

    if (theta > cutoff)
    {
        I_difusa = Ld * kd * max(dot(n, l), 0.0);

        if (dot(n, l) > 0.0) {
            I_especular = Ls * ks * pow(max(dot(v, r), 0.0), e);
        }
    }

    float luzTotal = I_ambiente + I_difusa + I_especular;
    luzTotal = clamp(luzTotal, 0.0, 1.0);

    FragColor = vec4(corTex.rgb * luzTotal, corTex.a);
}
