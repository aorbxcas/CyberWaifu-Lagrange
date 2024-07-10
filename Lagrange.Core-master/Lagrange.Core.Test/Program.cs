using Lagrange.Core.Test.Tests;
using System.Configuration;

namespace Lagrange.Core.Test;

internal static class Program
{
    public static async Task Main(string[] args)
    {
        // BenchmarkRunner.Run<ProtoBufTest>(new DebugBuildConfig());
        // await new WtLoginTest().FetchQrCode();
        await new NTLoginTest().LoginByPassword();

    }
}