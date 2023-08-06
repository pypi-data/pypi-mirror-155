/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES


namespace mlir {
class AsmParser;
class AsmPrinter;
} // namespace mlir
namespace mlir {
namespace lmhlo_gpu {
class ActivationAttr;
class ConvolutionBackendConfigAttr;
namespace detail {
struct ActivationAttrStorage;
} // namespace detail
class ActivationAttr : public ::mlir::Attribute::AttrBase<ActivationAttr, ::mlir::Attribute, detail::ActivationAttrStorage> {
public:
  using Base::Base;
public:
  static ActivationAttr get(::mlir::MLIRContext *context, ::mlir::lmhlo_gpu::Activation value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"activation"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::lmhlo_gpu::Activation getValue() const;
};
namespace detail {
struct ConvolutionBackendConfigAttrStorage;
} // namespace detail
class ConvolutionBackendConfigAttr : public ::mlir::Attribute::AttrBase<ConvolutionBackendConfigAttr, ::mlir::Attribute, detail::ConvolutionBackendConfigAttrStorage> {
public:
  using Base::Base;
public:
  static ConvolutionBackendConfigAttr get(::mlir::MLIRContext *context, int64_t algorithm, bool tensor_ops_enabled, ::llvm::ArrayRef<int64_t> knob_ids, ::llvm::ArrayRef<int64_t> knob_values, bool is_cudnn_frontend, int64_t workspace_size, ::llvm::ArrayRef<int64_t> operand_0_layout, ::llvm::ArrayRef<int64_t> operand_1_layout, ::llvm::ArrayRef<int64_t> result_layout);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"convolution_backend_config"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  int64_t getAlgorithm() const;
  bool getTensorOpsEnabled() const;
  ::llvm::ArrayRef<int64_t> getKnobIds() const;
  ::llvm::ArrayRef<int64_t> getKnobValues() const;
  bool getIsCudnnFrontend() const;
  int64_t getWorkspaceSize() const;
  ::llvm::ArrayRef<int64_t> getOperand_0Layout() const;
  ::llvm::ArrayRef<int64_t> getOperand_1Layout() const;
  ::llvm::ArrayRef<int64_t> getResultLayout() const;
};
} // namespace lmhlo_gpu
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::lmhlo_gpu::ActivationAttr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::lmhlo_gpu::ConvolutionBackendConfigAttr)

#endif  // GET_ATTRDEF_CLASSES

