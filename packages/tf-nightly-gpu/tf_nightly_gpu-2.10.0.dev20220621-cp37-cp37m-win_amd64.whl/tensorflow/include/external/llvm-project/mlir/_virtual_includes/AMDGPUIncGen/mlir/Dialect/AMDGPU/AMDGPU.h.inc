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
namespace amdgpu {
class RawBufferAtomicFaddOp;
} // namespace amdgpu
} // namespace mlir
namespace mlir {
namespace amdgpu {
class RawBufferLoadOp;
} // namespace amdgpu
} // namespace mlir
namespace mlir {
namespace amdgpu {
class RawBufferStoreOp;
} // namespace amdgpu
} // namespace mlir
#endif

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace amdgpu {

//===----------------------------------------------------------------------===//
// ::mlir::amdgpu::RawBufferAtomicFaddOp declarations
//===----------------------------------------------------------------------===//

class RawBufferAtomicFaddOpAdaptor {
public:
  RawBufferAtomicFaddOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  RawBufferAtomicFaddOpAdaptor(RawBufferAtomicFaddOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getValue();
  ::mlir::Value value();
  ::mlir::Value getMemref();
  ::mlir::Value memref();
  ::mlir::ValueRange getIndices();
  ::mlir::ValueRange indices();
  ::mlir::Value getSgprOffset();
  ::mlir::Value sgprOffset();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::BoolAttr getTargetIsRDNAAttr();
  bool getTargetIsRDNA();
  ::mlir::BoolAttr targetIsRDNAAttr();
  bool targetIsRDNA();
  ::mlir::BoolAttr getBoundsCheckAttr();
  bool getBoundsCheck();
  ::mlir::BoolAttr boundsCheckAttr();
  bool boundsCheck();
  ::mlir::IntegerAttr getIndexOffsetAttr();
  ::llvm::Optional<uint32_t> getIndexOffset();
  ::mlir::IntegerAttr indexOffsetAttr();
  ::llvm::Optional<uint32_t> indexOffset();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class RawBufferAtomicFaddOp : public ::mlir::Op<RawBufferAtomicFaddOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<2>::Impl, ::mlir::OpTrait::AttrSizedOperandSegments, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = RawBufferAtomicFaddOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("boundsCheck"), ::llvm::StringRef("indexOffset"), ::llvm::StringRef("operand_segment_sizes"), ::llvm::StringRef("targetIsRDNA")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getBoundsCheckAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getBoundsCheckAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr boundsCheckAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr boundsCheckAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getIndexOffsetAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getIndexOffsetAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr indexOffsetAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr indexOffsetAttrName(::mlir::OperationName name) {
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

  ::mlir::StringAttr getTargetIsRDNAAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getTargetIsRDNAAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr targetIsRDNAAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr targetIsRDNAAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("amdgpu.raw_buffer_atomic_fadd");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value getValue();
  ::mlir::Value value();
  ::mlir::Value getMemref();
  ::mlir::Value memref();
  ::mlir::Operation::operand_range getIndices();
  ::mlir::Operation::operand_range indices();
  ::mlir::Value getSgprOffset();
  ::mlir::Value sgprOffset();
  ::mlir::MutableOperandRange getValueMutable();
  ::mlir::MutableOperandRange valueMutable();
  ::mlir::MutableOperandRange getMemrefMutable();
  ::mlir::MutableOperandRange memrefMutable();
  ::mlir::MutableOperandRange getIndicesMutable();
  ::mlir::MutableOperandRange indicesMutable();
  ::mlir::MutableOperandRange getSgprOffsetMutable();
  ::mlir::MutableOperandRange sgprOffsetMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::BoolAttr getTargetIsRDNAAttr();
  bool getTargetIsRDNA();
  ::mlir::BoolAttr targetIsRDNAAttr();
  bool targetIsRDNA();
  ::mlir::BoolAttr getBoundsCheckAttr();
  bool getBoundsCheck();
  ::mlir::BoolAttr boundsCheckAttr();
  bool boundsCheck();
  ::mlir::IntegerAttr getIndexOffsetAttr();
  ::llvm::Optional<uint32_t> getIndexOffset();
  ::mlir::IntegerAttr indexOffsetAttr();
  ::llvm::Optional<uint32_t> indexOffset();
  void setTargetIsRDNAAttr(::mlir::BoolAttr attr);
  void targetIsRDNAAttr(::mlir::BoolAttr attr);
  void setBoundsCheckAttr(::mlir::BoolAttr attr);
  void boundsCheckAttr(::mlir::BoolAttr attr);
  void setIndexOffsetAttr(::mlir::IntegerAttr attr);
  void indexOffsetAttr(::mlir::IntegerAttr attr);
  ::mlir::Attribute removeIndexOffsetAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value value, ::mlir::Value memref, ::mlir::BoolAttr targetIsRDNA, ::mlir::ValueRange indices, ::mlir::BoolAttr boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value value, ::mlir::Value memref, ::mlir::BoolAttr targetIsRDNA, ::mlir::ValueRange indices, ::mlir::BoolAttr boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value value, ::mlir::Value memref, bool targetIsRDNA, ::mlir::ValueRange indices, bool boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value value, ::mlir::Value memref, bool targetIsRDNA, ::mlir::ValueRange indices, bool boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
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
    assert(index < 4 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace amdgpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::amdgpu::RawBufferAtomicFaddOp)

namespace mlir {
namespace amdgpu {

//===----------------------------------------------------------------------===//
// ::mlir::amdgpu::RawBufferLoadOp declarations
//===----------------------------------------------------------------------===//

class RawBufferLoadOpAdaptor {
public:
  RawBufferLoadOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  RawBufferLoadOpAdaptor(RawBufferLoadOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getMemref();
  ::mlir::Value memref();
  ::mlir::ValueRange getIndices();
  ::mlir::ValueRange indices();
  ::mlir::Value getSgprOffset();
  ::mlir::Value sgprOffset();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::BoolAttr getTargetIsRDNAAttr();
  bool getTargetIsRDNA();
  ::mlir::BoolAttr targetIsRDNAAttr();
  bool targetIsRDNA();
  ::mlir::BoolAttr getBoundsCheckAttr();
  bool getBoundsCheck();
  ::mlir::BoolAttr boundsCheckAttr();
  bool boundsCheck();
  ::mlir::IntegerAttr getIndexOffsetAttr();
  ::llvm::Optional<uint32_t> getIndexOffset();
  ::mlir::IntegerAttr indexOffsetAttr();
  ::llvm::Optional<uint32_t> indexOffset();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class RawBufferLoadOp : public ::mlir::Op<RawBufferLoadOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::Type>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<1>::Impl, ::mlir::OpTrait::AttrSizedOperandSegments, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = RawBufferLoadOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("boundsCheck"), ::llvm::StringRef("indexOffset"), ::llvm::StringRef("operand_segment_sizes"), ::llvm::StringRef("targetIsRDNA")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getBoundsCheckAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getBoundsCheckAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr boundsCheckAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr boundsCheckAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getIndexOffsetAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getIndexOffsetAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr indexOffsetAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr indexOffsetAttrName(::mlir::OperationName name) {
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

  ::mlir::StringAttr getTargetIsRDNAAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getTargetIsRDNAAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr targetIsRDNAAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr targetIsRDNAAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("amdgpu.raw_buffer_load");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value getMemref();
  ::mlir::Value memref();
  ::mlir::Operation::operand_range getIndices();
  ::mlir::Operation::operand_range indices();
  ::mlir::Value getSgprOffset();
  ::mlir::Value sgprOffset();
  ::mlir::MutableOperandRange getMemrefMutable();
  ::mlir::MutableOperandRange memrefMutable();
  ::mlir::MutableOperandRange getIndicesMutable();
  ::mlir::MutableOperandRange indicesMutable();
  ::mlir::MutableOperandRange getSgprOffsetMutable();
  ::mlir::MutableOperandRange sgprOffsetMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Value getValue();
  ::mlir::Value value();
  ::mlir::BoolAttr getTargetIsRDNAAttr();
  bool getTargetIsRDNA();
  ::mlir::BoolAttr targetIsRDNAAttr();
  bool targetIsRDNA();
  ::mlir::BoolAttr getBoundsCheckAttr();
  bool getBoundsCheck();
  ::mlir::BoolAttr boundsCheckAttr();
  bool boundsCheck();
  ::mlir::IntegerAttr getIndexOffsetAttr();
  ::llvm::Optional<uint32_t> getIndexOffset();
  ::mlir::IntegerAttr indexOffsetAttr();
  ::llvm::Optional<uint32_t> indexOffset();
  void setTargetIsRDNAAttr(::mlir::BoolAttr attr);
  void targetIsRDNAAttr(::mlir::BoolAttr attr);
  void setBoundsCheckAttr(::mlir::BoolAttr attr);
  void boundsCheckAttr(::mlir::BoolAttr attr);
  void setIndexOffsetAttr(::mlir::IntegerAttr attr);
  void indexOffsetAttr(::mlir::IntegerAttr attr);
  ::mlir::Attribute removeIndexOffsetAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type value, ::mlir::Value memref, ::mlir::BoolAttr targetIsRDNA, ::mlir::ValueRange indices, ::mlir::BoolAttr boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value memref, ::mlir::BoolAttr targetIsRDNA, ::mlir::ValueRange indices, ::mlir::BoolAttr boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type value, ::mlir::Value memref, bool targetIsRDNA, ::mlir::ValueRange indices, bool boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value memref, bool targetIsRDNA, ::mlir::ValueRange indices, bool boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
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
    assert(index < 4 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace amdgpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::amdgpu::RawBufferLoadOp)

namespace mlir {
namespace amdgpu {

//===----------------------------------------------------------------------===//
// ::mlir::amdgpu::RawBufferStoreOp declarations
//===----------------------------------------------------------------------===//

class RawBufferStoreOpAdaptor {
public:
  RawBufferStoreOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  RawBufferStoreOpAdaptor(RawBufferStoreOp op);

  ::mlir::ValueRange getOperands();
  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getValue();
  ::mlir::Value value();
  ::mlir::Value getMemref();
  ::mlir::Value memref();
  ::mlir::ValueRange getIndices();
  ::mlir::ValueRange indices();
  ::mlir::Value getSgprOffset();
  ::mlir::Value sgprOffset();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::BoolAttr getTargetIsRDNAAttr();
  bool getTargetIsRDNA();
  ::mlir::BoolAttr targetIsRDNAAttr();
  bool targetIsRDNA();
  ::mlir::BoolAttr getBoundsCheckAttr();
  bool getBoundsCheck();
  ::mlir::BoolAttr boundsCheckAttr();
  bool boundsCheck();
  ::mlir::IntegerAttr getIndexOffsetAttr();
  ::llvm::Optional<uint32_t> getIndexOffset();
  ::mlir::IntegerAttr indexOffsetAttr();
  ::llvm::Optional<uint32_t> indexOffset();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class RawBufferStoreOp : public ::mlir::Op<RawBufferStoreOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<2>::Impl, ::mlir::OpTrait::AttrSizedOperandSegments, ::mlir::OpTrait::OpInvariants, ::mlir::MemoryEffectOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = RawBufferStoreOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("boundsCheck"), ::llvm::StringRef("indexOffset"), ::llvm::StringRef("operand_segment_sizes"), ::llvm::StringRef("targetIsRDNA")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getBoundsCheckAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getBoundsCheckAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr boundsCheckAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr boundsCheckAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getIndexOffsetAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getIndexOffsetAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr indexOffsetAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr indexOffsetAttrName(::mlir::OperationName name) {
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

  ::mlir::StringAttr getTargetIsRDNAAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr getTargetIsRDNAAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  ::mlir::StringAttr targetIsRDNAAttrName() {
    return getAttributeNameForIndex(3);
  }

  static ::mlir::StringAttr targetIsRDNAAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 3);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("amdgpu.raw_buffer_store");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Value getValue();
  ::mlir::Value value();
  ::mlir::Value getMemref();
  ::mlir::Value memref();
  ::mlir::Operation::operand_range getIndices();
  ::mlir::Operation::operand_range indices();
  ::mlir::Value getSgprOffset();
  ::mlir::Value sgprOffset();
  ::mlir::MutableOperandRange getValueMutable();
  ::mlir::MutableOperandRange valueMutable();
  ::mlir::MutableOperandRange getMemrefMutable();
  ::mlir::MutableOperandRange memrefMutable();
  ::mlir::MutableOperandRange getIndicesMutable();
  ::mlir::MutableOperandRange indicesMutable();
  ::mlir::MutableOperandRange getSgprOffsetMutable();
  ::mlir::MutableOperandRange sgprOffsetMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::BoolAttr getTargetIsRDNAAttr();
  bool getTargetIsRDNA();
  ::mlir::BoolAttr targetIsRDNAAttr();
  bool targetIsRDNA();
  ::mlir::BoolAttr getBoundsCheckAttr();
  bool getBoundsCheck();
  ::mlir::BoolAttr boundsCheckAttr();
  bool boundsCheck();
  ::mlir::IntegerAttr getIndexOffsetAttr();
  ::llvm::Optional<uint32_t> getIndexOffset();
  ::mlir::IntegerAttr indexOffsetAttr();
  ::llvm::Optional<uint32_t> indexOffset();
  void setTargetIsRDNAAttr(::mlir::BoolAttr attr);
  void targetIsRDNAAttr(::mlir::BoolAttr attr);
  void setBoundsCheckAttr(::mlir::BoolAttr attr);
  void boundsCheckAttr(::mlir::BoolAttr attr);
  void setIndexOffsetAttr(::mlir::IntegerAttr attr);
  void indexOffsetAttr(::mlir::IntegerAttr attr);
  ::mlir::Attribute removeIndexOffsetAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value value, ::mlir::Value memref, ::mlir::BoolAttr targetIsRDNA, ::mlir::ValueRange indices, ::mlir::BoolAttr boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value value, ::mlir::Value memref, ::mlir::BoolAttr targetIsRDNA, ::mlir::ValueRange indices, ::mlir::BoolAttr boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value value, ::mlir::Value memref, bool targetIsRDNA, ::mlir::ValueRange indices, bool boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value value, ::mlir::Value memref, bool targetIsRDNA, ::mlir::ValueRange indices, bool boundsCheck, /*optional*/::mlir::IntegerAttr indexOffset, /*optional*/::mlir::Value sgprOffset);
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
    assert(index < 4 && "invalid attribute index");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:
};
} // namespace amdgpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::amdgpu::RawBufferStoreOp)


#endif  // GET_OP_CLASSES

