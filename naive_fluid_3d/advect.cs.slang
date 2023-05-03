import common;

Texture3D<float4> Velocity;
Texture3D<float4> Data;

RWTexture3D<float4> OutVelocity;
RWTexture3D<float4> OutData;


[numthreads(8, 8, 8)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if(thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z)
        return;

    float3 velocity = Velocity[thread_id.xyz].xyz;
    float3 delta_pos = velocity * DELTA_TIME / CELL_SIZE;
    float3 last_pos = thread_id.xyz - delta_pos;

    OutVelocity[thread_id.xyz] = Velocity.Load(last_pos) * 0.9999;
    OutData[thread_id.xyz] = Data.Load(last_pos) * 0.9999;
}
