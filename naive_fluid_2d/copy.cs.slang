import common;

Texture2D<float4> Source;
RWTexture2D<float4> Dest;

[numthreads(8, 8, 1)]
void main(uint3 thread_id: SV_DispatchThreadID)
{
    if(thread_id.x >= iThreads.x || thread_id.y >= iThreads.y)
        return;
    Dest[thread_id.xy] = Source.Load(thread_id.xy);
}
