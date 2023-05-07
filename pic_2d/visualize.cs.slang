import common;

Texture2D<float4> GridVelocity;
RWTexture2D<float4> Out;

[numthreads(8, 8, 1)]
void main(uint3 thread_id: SV_DispatchThreadID) {
    if (thread_id.x >= iThreads.x || thread_id.y >= iThreads.y || thread_id.z >= iThreads.z) {
        return;
    }
}