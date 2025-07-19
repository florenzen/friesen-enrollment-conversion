#!/bin/bash

# Build script wrapper for Friesen Enrollment Converter on macOS
# This script provides an easy way to build the macOS app bundle and DMG

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing build dependencies..."
    
    # Check if pip is available
    if ! command_exists pip3; then
        print_error "pip3 not found. Please install Python 3 with pip."
        exit 1
    fi
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    pip3 install -r ../common/requirements-build.txt
    
    # Check if create-dmg is installed
    if ! command_exists create-dmg; then
        print_warning "create-dmg not found. Installing via Homebrew..."
        
        if ! command_exists brew; then
            print_error "Homebrew not found. Please install Homebrew first:"
            print_error "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
        
        brew install create-dmg
    fi
    
    print_success "Dependencies installed successfully!"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --install-deps    Install build dependencies"
    echo "  --clean           Clean build directories only"
    echo "  --skip-deps       Skip dependency installation"
    echo "  --skip-codesign   Skip codesigning"
    echo "  --skip-dmg        Skip DMG creation"
    echo "  --version VERSION Override version number"
    echo "  --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                    # Full build with default settings"
    echo "  $0 --install-deps     # Install dependencies only"
    echo "  $0 --version 1.1.0    # Build with specific version"
    echo "  $0 --skip-dmg         # Build app bundle only (no DMG)"
    echo "  $0 --clean            # Clean build directories"
}

# Parse command line arguments
INSTALL_DEPS=false
CLEAN_ONLY=false
SKIP_DEPS=false
SKIP_CODESIGN=false
SKIP_DMG=false
VERSION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --install-deps)
            INSTALL_DEPS=true
            shift
            ;;
        --clean)
            CLEAN_ONLY=true
            shift
            ;;
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        --skip-codesign)
            SKIP_CODESIGN=true
            shift
            ;;
        --skip-dmg)
            SKIP_DMG=true
            shift
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only"
    exit 1
fi

# Main script logic
if [ "$INSTALL_DEPS" = true ]; then
    install_dependencies
    exit 0
fi

# Check if Python script exists
if [ ! -f "build.py" ]; then
    print_error "build.py not found. Please run this script from the build/macos directory."
    exit 1
fi

# Build the application
print_status "Starting build process..."

# Construct Python command
PYTHON_CMD="python3 build.py"

if [ "$CLEAN_ONLY" = true ]; then
    PYTHON_CMD="$PYTHON_CMD --clean"
else
    if [ "$SKIP_DEPS" = true ]; then
        PYTHON_CMD="$PYTHON_CMD --skip-deps"
    fi
    
    if [ "$SKIP_CODESIGN" = true ]; then
        PYTHON_CMD="$PYTHON_CMD --skip-codesign"
    fi
    
    if [ "$SKIP_DMG" = true ]; then
        PYTHON_CMD="$PYTHON_CMD --skip-dmg"
    fi
    
    if [ -n "$VERSION" ]; then
        PYTHON_CMD="$PYTHON_CMD --version $VERSION"
    fi
fi

# Run the Python build script
print_status "Running: $PYTHON_CMD"
eval $PYTHON_CMD

if [ $? -eq 0 ]; then
    print_success "Build completed successfully!"
else
    print_error "Build failed!"
    exit 1
fi 