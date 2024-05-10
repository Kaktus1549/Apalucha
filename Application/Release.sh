read -p "Enter target directory (default: ./Release/): " target
target=${target:-./Release/}

# For Windows x64
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -p:AssemblyName=Apalucha-win-x64 -p:DebugType=none -o $target

# For Windows ARM64
dotnet publish -c Release -r win-arm64 --self-contained true -p:PublishSingleFile=true -p:AssemblyName=Apalucha-win-arm64 -p:DebugType=none -o $target

# For Linux x64
dotnet publish -c Release -r linux-x64 --self-contained true -p:PublishSingleFile=true -p:AssemblyName=Apalucha-linux-x64 -p:DebugType=none -o $target

# For Linux ARM64
dotnet publish -c Release -r linux-arm64 --self-contained true -p:PublishSingleFile=true -p:AssemblyName=Apalucha-linux-arm64 -p:DebugType=none -o $target

# For macOS x64
dotnet publish -c Release -r osx-x64 --self-contained true -p:PublishSingleFile=true -p:AssemblyName=Apalucha-macos-x64 -p:DebugType=none -o $target

# For macOS ARM64
dotnet publish -c Release -r osx-arm64 --self-contained true -p:PublishSingleFile=true -p:AssemblyName=Apalucha-macos-arm64 -p:DebugType=none -o $target
