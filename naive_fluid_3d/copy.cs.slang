import common;

Texture3D<float4> Source;
RWTexture3D<float4> Dest;

[numthreads(8, 8, 8)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if (thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z)
        return;
 
    Dest[thread_id.xyz] = Source.Load(thread_id.xyz);
}
