import common;

struct VsOut
{
    float2 uv : TEXCOORD;
    float4 position : SV_POSITION;
};

Texture3D<float4> Velocity;
Texture3D<float4> Data;

static constexpr float4x4 INV_WORLD = float4x4(
    0.078125, 0., 0., 0.5,
    0., 0.078125, 0., 0.5,
    0., 0., 0.078125, 0.5,
    0., 0., 0., 1.
);

float4 main(VsOut in) : SV_Target {
    float3 value = float3(1, 1, 1);

    uint steps = 100;
    float march_length = CELL_SIZE * length(Data.GetDimensions()) * 0.6;
    float step_size = march_length / steps;

    let ray = get_camera_ray(in.uv);

    for (int i = 0; i < steps; i++) {
        let world_pos = ray.origin + ray.direction * step_size * (i + 1);
        let local_pos = mul(INV_WORLD, float4(world_pos, 1));
        let uv3 = float3(local_pos.xyz / local_pos.w);
        float4 sample = Data.SampleLevel0(uv3);
        value *= exp(-sample.xyz * step_size);
    }

    return float4(value, 1);
}