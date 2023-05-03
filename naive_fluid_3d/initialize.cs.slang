import common;

RWTexture3D<float4> Velocity;
RWTexture3D<float4> Data;

[numthreads(8, 8, 8)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if (thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z)
        return;

    // Velocity[thread_id.xy] = float4(0, 0, 0, 0);
    // Data[thread_id.xy] = float4(0, 0, 0, 0);
}
