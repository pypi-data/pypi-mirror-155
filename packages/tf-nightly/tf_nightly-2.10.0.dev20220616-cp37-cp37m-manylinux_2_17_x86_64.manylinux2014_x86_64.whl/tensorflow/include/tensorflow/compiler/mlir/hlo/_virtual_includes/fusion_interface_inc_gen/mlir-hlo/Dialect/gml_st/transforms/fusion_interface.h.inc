/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace gml_st {
class FusionIterface;
namespace detail {
struct FusionIterfaceInterfaceTraits {
  struct Concept {
    ::mlir::Value (*fuse)(const Concept *impl, ::mlir::Operation *, ::mlir::Location, ::mlir::Value, OpBuilder&);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = ::mlir::gml_st::FusionIterface;
    Model() : Concept{fuse} {}

    static inline ::mlir::Value fuse(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Location loc, ::mlir::Value subset, OpBuilder& builder);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = ::mlir::gml_st::FusionIterface;
    FallbackModel() : Concept{fuse} {}

    static inline ::mlir::Value fuse(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Location loc, ::mlir::Value subset, OpBuilder& builder);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
  };
};template <typename ConcreteOp>
struct FusionIterfaceTrait;

} // namespace detail
class FusionIterface : public ::mlir::OpInterface<FusionIterface, detail::FusionIterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<FusionIterface, detail::FusionIterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::FusionIterfaceTrait<ConcreteOp> {};
  ::mlir::Value fuse(::mlir::Location loc, ::mlir::Value subset, OpBuilder& builder);
};
namespace detail {
  template <typename ConcreteOp>
  struct FusionIterfaceTrait : public ::mlir::OpInterface<FusionIterface, detail::FusionIterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
template<typename ConcreteOp>
::mlir::Value detail::FusionIterfaceInterfaceTraits::Model<ConcreteOp>::fuse(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Location loc, ::mlir::Value subset, OpBuilder& builder) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).fuse(loc, subset, builder);
}
template<typename ConcreteOp>
::mlir::Value detail::FusionIterfaceInterfaceTraits::FallbackModel<ConcreteOp>::fuse(const Concept *impl, ::mlir::Operation *tablegen_opaque_val, ::mlir::Location loc, ::mlir::Value subset, OpBuilder& builder) {
  return static_cast<const ConcreteOp *>(impl)->fuse(tablegen_opaque_val, loc, subset, builder);
}
} // namespace gml_st
} // namespace mlir
