import common;

RWTexture2D<float4> Velocity;
RWTexture2D<float4> Data;

[numthreads(8, 8, 1)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if(thread_id.x >= iThreads.x || thread_id.y >= iThreads.y)
        return;

    // Velocity[thread_id.xy] = float4(0, 0, 0, 0);
    // Data[thread_id.xy] = float4(0, 0, 0, 0);
}
