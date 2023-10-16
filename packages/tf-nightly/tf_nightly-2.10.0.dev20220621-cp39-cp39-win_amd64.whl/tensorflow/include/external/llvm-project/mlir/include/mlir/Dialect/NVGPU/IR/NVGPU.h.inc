/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Declarations                                                            *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#if defined(GET_OP_CLASSES) || defined(GET_OP_FWD_DEFINES)
#undef GET_OP_FWD_DEFINES
namespace mlir {
namespace nvgpu {
class DeviceAsyncCopyOp;
} // namespace nvgpu
} // namespace mlir
namespace mlir {
namespace nvgpu {
class DeviceAsyncCreateGroupOp;
} // namespace nvgpu
} // namespace mlir
namespace mlir {
namespace nvgpu {
class DeviceAsyncWaitOp;
} // namespace nvgpu
} // namespace mlir
namespace mlir {
namespace nvgpu {
class LdMatrixOp;
} // namespace nvgpu
} // namespace mlir
namespace mlir {
namespace nvgpu {
class MmaSyncOp;
} // namespace nvgpu
} // namespace mlir
#endif

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace nvgpu {

//===----------------------------------------------------------------------===//
// ::mlir::nvgpu::DeviceAsyncCopyOp declarations
//===----------------------------------------------------------------------===//

class DeviceAsyncCopyOpAdaptor {
public:
  DeviceAsyncCopyOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  DeviceAsyncCopyOpAdaptor(DeviceAsyncCopyOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getDst();
  ::mlir::Value dst();
  ::mlir::ValueRange getDstIndices();
  ::mlir::ValueRange dstIndices();
  ::mlir::Value getSrc();
  ::mlir::Value src();
  ::mlir::ValueRange getSrcIndices();
  ::mlir::ValueRange srcIndices();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::IntegerAttr getNumElementsAttr();
  ::llvm::APInt getNumElements();
  ::mlir::IntegerAttr numElementsAttr();
  ::llvm::APInt numElements();
  ::mlir::UnitAttr getBypassL1Attr();
  ::llvm::Optional<bool> getBypassL1();
  ::mlir::UnitAttr bypassL1Attr();
  ::llvm::Optional<bool> bypassL1();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class DeviceAsyncCopyOp : public ::mlir::Op<DeviceAsyncCopyOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::Type>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<2>::Impl, ::mlir::OpTrait::AttrSizedOperandSegments, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = DeviceAsyncCopyOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("bypassL1"), ::llvm::StringRef("numElements"), ::llvm::StringRef("operand_segment_sizes")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getBypassL1AttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getBypassL1AttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr bypassL1AttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr bypassL1AttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getNumElementsAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getNumElementsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr numElementsAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr numElementsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getOperandSegmentSizesAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getOperandSegmentSizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  ::mlir::StringAttr operand_segment_sizesAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr operand_segment_sizesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("nvgpu.device_async_copy");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value getDst();
  ::mlir::Value dst();
  ::mlir::Operation::operand_range getDstIndices();
  ::mlir::Operation::operand_range dstIndices();
  ::mlir::Value getSrc();
  ::mlir::Value src();
  ::mlir::Operation::operand_range getSrcIndices();
  ::mlir::Operation::operand_range srcIndices();
  ::mlir::MutableOperandRange getDstMutable();
  ::mlir::MutableOperandRange dstMutable();
  ::mlir::MutableOperandRange getDstIndicesMutable();
  ::mlir::MutableOperandRange dstIndicesMutable();
  ::mlir::MutableOperandRange getSrcMutable();
  ::mlir::MutableOperandRange srcMutable();
  ::mlir::MutableOperandRange getSrcIndicesMutable();
  ::mlir::MutableOperandRange srcIndicesMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Value getAsyncToken();
  ::mlir::Value asyncToken();
  ::mlir::IntegerAttr getNumElementsAttr();
  ::llvm::APInt getNumElements();
  ::mlir::IntegerAttr numElementsAttr();
  ::llvm::APInt numElements();
  ::mlir::UnitAttr getBypassL1Attr();
  ::llvm::Optional<bool> getBypassL1();
  ::mlir::UnitAttr bypassL1Attr();
  ::llvm::Optional<bool> bypassL1();
  void setNumElementsAttr(::mlir::IntegerAttr attr);
  void numElementsAttr(::mlir::IntegerAttr attr);
  void setBypassL1Attr(::mlir::UnitAttr attr);
  void bypassL1Attr(::mlir::UnitAttr attr);
  ::mlir::Attribute removeBypassL1Attr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type asyncToken, ::mlir::Value dst, ::mlir::ValueRange dstIndices, ::mlir::Value src, ::mlir::ValueRange srcIndices, ::mlir::IntegerAttr numElements, /*optional*/::mlir::UnitAttr bypassL1);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value dst, ::mlir::ValueRange dstIndices, ::mlir::Value src, ::mlir::ValueRange srcIndices, ::mlir::IntegerAttr numElements, /*optional*/::mlir::UnitAttr bypassL1);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type asyncToken, ::mlir::Value dst, ::mlir::ValueRange dstIndices, ::mlir::Value src, ::mlir::ValueRange srcIndices, ::llvm::APInt numElements, /*optional*/::mlir::UnitAttr bypassL1);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value dst, ::mlir::ValueRange dstIndices, ::mlir::Value src, ::mlir::ValueRange srcIndices, ::llvm::APInt numElements, /*optional*/::mlir::UnitAttr bypassL1);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace nvgpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::nvgpu::DeviceAsyncCopyOp)

namespace mlir {
namespace nvgpu {

//===----------------------------------------------------------------------===//
// ::mlir::nvgpu::DeviceAsyncCreateGroupOp declarations
//===----------------------------------------------------------------------===//

class DeviceAsyncCreateGroupOpAdaptor {
public:
  DeviceAsyncCreateGroupOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  DeviceAsyncCreateGroupOpAdaptor(DeviceAsyncCreateGroupOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getInputTokens();
  ::mlir::ValueRange inputTokens();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class DeviceAsyncCreateGroupOp : public ::mlir::Op<DeviceAsyncCreateGroupOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::Type>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = DeviceAsyncCreateGroupOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("nvgpu.device_async_create_group");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getInputTokens();
  ::mlir::Operation::operand_range inputTokens();
  ::mlir::MutableOperandRange getInputTokensMutable();
  ::mlir::MutableOperandRange inputTokensMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Value getAsyncToken();
  ::mlir::Value asyncToken();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type asyncToken, ::mlir::ValueRange inputTokens);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
public:
};
} // namespace nvgpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::nvgpu::DeviceAsyncCreateGroupOp)

namespace mlir {
namespace nvgpu {

//===----------------------------------------------------------------------===//
// ::mlir::nvgpu::DeviceAsyncWaitOp declarations
//===----------------------------------------------------------------------===//

class DeviceAsyncWaitOpAdaptor {
public:
  DeviceAsyncWaitOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  DeviceAsyncWaitOpAdaptor(DeviceAsyncWaitOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getAsyncDependencies();
  ::mlir::Value asyncDependencies();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::IntegerAttr getNumGroupsAttr();
  ::llvm::Optional<uint32_t> getNumGroups();
  ::mlir::IntegerAttr numGroupsAttr();
  ::llvm::Optional<uint32_t> numGroups();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class DeviceAsyncWaitOp : public ::mlir::Op<DeviceAsyncWaitOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::OneOperand, ::mlir::OpTrait::OpInvariants> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = DeviceAsyncWaitOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("numGroups")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getNumGroupsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getNumGroupsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr numGroupsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr numGroupsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("nvgpu.device_async_wait");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value getAsyncDependencies();
  ::mlir::Value asyncDependencies();
  ::mlir::MutableOperandRange getAsyncDependenciesMutable();
  ::mlir::MutableOperandRange asyncDependenciesMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::IntegerAttr getNumGroupsAttr();
  ::llvm::Optional<uint32_t> getNumGroups();
  ::mlir::IntegerAttr numGroupsAttr();
  ::llvm::Optional<uint32_t> numGroups();
  void setNumGroupsAttr(::mlir::IntegerAttr attr);
  void numGroupsAttr(::mlir::IntegerAttr attr);
  ::mlir::Attribute removeNumGroupsAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value asyncDependencies, /*optional*/::mlir::IntegerAttr numGroups);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value asyncDependencies, /*optional*/::mlir::IntegerAttr numGroups);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace nvgpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::nvgpu::DeviceAsyncWaitOp)

namespace mlir {
namespace nvgpu {

//===----------------------------------------------------------------------===//
// ::mlir::nvgpu::LdMatrixOp declarations
//===----------------------------------------------------------------------===//

class LdMatrixOpAdaptor {
public:
  LdMatrixOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  LdMatrixOpAdaptor(LdMatrixOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getSrcMemref();
  ::mlir::Value srcMemref();
  ::mlir::ValueRange getIndices();
  ::mlir::ValueRange indices();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::BoolAttr getTransposeAttr();
  bool getTranspose();
  ::mlir::BoolAttr transposeAttr();
  bool transpose();
  ::mlir::IntegerAttr getNumTilesAttr();
  uint32_t getNumTiles();
  ::mlir::IntegerAttr numTilesAttr();
  uint32_t numTiles();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class LdMatrixOp : public ::mlir::Op<LdMatrixOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::VectorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<1>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = LdMatrixOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("numTiles"), ::llvm::StringRef("transpose")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getNumTilesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getNumTilesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr numTilesAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr numTilesAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getTransposeAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getTransposeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr transposeAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr transposeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("nvgpu.ldmatrix");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value getSrcMemref();
  ::mlir::Value srcMemref();
  ::mlir::Operation::operand_range getIndices();
  ::mlir::Operation::operand_range indices();
  ::mlir::MutableOperandRange getSrcMemrefMutable();
  ::mlir::MutableOperandRange srcMemrefMutable();
  ::mlir::MutableOperandRange getIndicesMutable();
  ::mlir::MutableOperandRange indicesMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Value getRes();
  ::mlir::Value res();
  ::mlir::BoolAttr getTransposeAttr();
  bool getTranspose();
  ::mlir::BoolAttr transposeAttr();
  bool transpose();
  ::mlir::IntegerAttr getNumTilesAttr();
  uint32_t getNumTiles();
  ::mlir::IntegerAttr numTilesAttr();
  uint32_t numTiles();
  void setTransposeAttr(::mlir::BoolAttr attr);
  void transposeAttr(::mlir::BoolAttr attr);
  void setNumTilesAttr(::mlir::IntegerAttr attr);
  void numTilesAttr(::mlir::IntegerAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type res, ::mlir::Value srcMemref, ::mlir::ValueRange indices, ::mlir::BoolAttr transpose, ::mlir::IntegerAttr numTiles);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value srcMemref, ::mlir::ValueRange indices, ::mlir::BoolAttr transpose, ::mlir::IntegerAttr numTiles);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type res, ::mlir::Value srcMemref, ::mlir::ValueRange indices, bool transpose, uint32_t numTiles);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value srcMemref, ::mlir::ValueRange indices, bool transpose, uint32_t numTiles);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 2 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace nvgpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::nvgpu::LdMatrixOp)

namespace mlir {
namespace nvgpu {

//===----------------------------------------------------------------------===//
// ::mlir::nvgpu::MmaSyncOp declarations
//===----------------------------------------------------------------------===//

class MmaSyncOpAdaptor {
public:
  MmaSyncOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  MmaSyncOpAdaptor(MmaSyncOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getMatrixA();
  ::mlir::Value matrixA();
  ::mlir::Value getMatrixB();
  ::mlir::Value matrixB();
  ::mlir::Value getMatrixC();
  ::mlir::Value matrixC();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::ArrayAttr getMmaShapeAttr();
  ::mlir::ArrayAttr getMmaShape();
  ::mlir::ArrayAttr mmaShapeAttr();
  ::mlir::ArrayAttr mmaShape();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class MmaSyncOp : public ::mlir::Op<MmaSyncOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::VectorType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::NOperands<3>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = MmaSyncOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("mmaShape")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getMmaShapeAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getMmaShapeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr mmaShapeAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr mmaShapeAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("nvgpu.mma.sync");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value getMatrixA();
  ::mlir::Value matrixA();
  ::mlir::Value getMatrixB();
  ::mlir::Value matrixB();
  ::mlir::Value getMatrixC();
  ::mlir::Value matrixC();
  ::mlir::MutableOperandRange getMatrixAMutable();
  ::mlir::MutableOperandRange matrixAMutable();
  ::mlir::MutableOperandRange getMatrixBMutable();
  ::mlir::MutableOperandRange matrixBMutable();
  ::mlir::MutableOperandRange getMatrixCMutable();
  ::mlir::MutableOperandRange matrixCMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Value getRes();
  ::mlir::Value res();
  ::mlir::ArrayAttr getMmaShapeAttr();
  ::mlir::ArrayAttr getMmaShape();
  ::mlir::ArrayAttr mmaShapeAttr();
  ::mlir::ArrayAttr mmaShape();
  void setMmaShapeAttr(::mlir::ArrayAttr attr);
  void mmaShapeAttr(::mlir::ArrayAttr attr);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type res, ::mlir::Value matrixA, ::mlir::Value matrixB, ::mlir::Value matrixC, ::mlir::ArrayAttr mmaShape);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value matrixA, ::mlir::Value matrixB, ::mlir::Value matrixC, ::mlir::ArrayAttr mmaShape);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace nvgpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::nvgpu::MmaSyncOp)


#endif  // GET_OP_CLASSES

