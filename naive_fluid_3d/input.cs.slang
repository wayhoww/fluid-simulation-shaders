import common;

RWTexture3D<float4> Velocity;
RWTexture3D<float4> Data;

[numthreads(8, 8, 8)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if (thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z)
        return;

    let thread_uv = 1.0f * thread_id.xyz / iThreads.xyz;

    if (length(thread_uv - float3(0.2, 0.5, 0.5)) < 0.1) {
        Velocity[thread_id.xyz] = float4(3, 0, 0, 0);
        Data[thread_id.xyz] = float4(0, 2, 2, 1);
    }
    if (length(thread_uv - float3(0.8, 0.3, 0.5)) < 0.1) {
        Velocity[thread_id.xyz] = float4(-3, 2, 0, 0);
        Data[thread_id.xyz] = float4(2, 2, 0, 1);
    }
    if (length(thread_uv - float3(0.5, 0.5, 0.2)) < 0.1) {
        Velocity[thread_id.xyz] = float4(0, 0, 2, 0);
        Data[thread_id.xyz] = float4(2, 0, 2, 1);
    }
}
