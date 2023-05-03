import common;

Texture3D<float4> Velocity;
RWTexture3D<float4> OutDivergence;

[numthreads(8, 8, 8)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if (thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z)
        return;

    float3 vel_0 = Velocity[thread_id.xyz + int3( 1, 0, 0)].xyz;
    float3 vel_1 = Velocity[thread_id.xyz + int3(-1, 0, 0)].xyz;
    float3 vel_2 = Velocity[thread_id.xyz + int3(0,  1, 0)].xyz;
    float3 vel_3 = Velocity[thread_id.xyz + int3(0, -1, 0)].xyz;
    float3 vel_4 = Velocity[thread_id.xyz + int3(0, 0,  1)].xyz;
    float3 vel_5 = Velocity[thread_id.xyz + int3(0, 0, -1)].xyz;

    float divergence = 0.5 * (vel_0.x - vel_1.x + vel_2.y - vel_3.y + vel_4.z - vel_5.z) / CELL_SIZE;

    OutDivergence[thread_id.xyz] = float4(divergence, 0.0f, 0.0f, 0.0f);
}
