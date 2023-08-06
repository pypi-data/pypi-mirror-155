#ifndef DS_TUPLE_VINEYARD_H
#define DS_TUPLE_VINEYARD_H

/** Copyright 2020-2021 Alibaba Group Holding Limited.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#ifndef MODULES_BASIC_DS_TUPLE_MOD_H_
#define MODULES_BASIC_DS_TUPLE_MOD_H_

#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "client/client.h"
#include "client/ds/blob.h"
#include "client/ds/i_object.h"
#include "common/util/logging.h"
#include "common/util/uuid.h"

namespace vineyard {

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

class TupleBaseBuilder;

/**
 * @brief The tuple type in vineyard
 *
 */
class Tuple : public Registered<Tuple> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<Tuple>{
                new Tuple()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<Tuple>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        meta.GetKeyValue("size_", this->size_);
        for (size_t __idx = 0; __idx < meta.GetKeyValue<size_t>("__elements_-size"); ++__idx) {
            this->elements_.emplace_back(std::dynamic_pointer_cast<Object>(
                    meta.GetMember("__elements_-" + std::to_string(__idx))));
        }

        
    }

 private:
public:
  /**
   * @brief Get the size of the tuple, i.e., the number of elements it contains.
   *
   * @return The size of the tuple.
   */
  size_t const Size() const { return this->size_; }

  /**
   * @brief Get the value at the given index.
   *
   * @param index The given index to get the value.
   */
  std::shared_ptr<Object> const At(size_t index) const {
    if (index >= size_) {
      LOG(ERROR) << "tuple::at(): out of range: " << index;
      return nullptr;
    }
    return elements_[index];
  }

  /**
   * @brief The iterator for the tuple object to iterate from the first to the
   * last element.
   *
   */
  class iterator
      : public std::iterator<
            std::bidirectional_iterator_tag, std::shared_ptr<Object>, size_t,
            const std::shared_ptr<Object>*, std::shared_ptr<Object>> {
    Tuple const* tuple_;
    size_t index_;

   public:
    explicit iterator(Tuple const* tuple, size_t index = 0)
        : tuple_(tuple), index_(index) {}
    iterator& operator++() {
      index_ += 1;
      return *this;
    }
    bool operator==(iterator other) const { return index_ == other.index_; }
    bool operator!=(iterator other) const { return index_ != other.index_; }
    reference operator*() const { return tuple_->At(index_); }
  };

  /**
   * @brief Get the beginning iterator.
   *
   * @return The beginning iterrator.
   */
  const iterator begin() const { return iterator(this, 0); }

  /**
   * @brief Get the ending iterator.
   *
   * @return The ending iterator.
   */
  const iterator end() const { return iterator(this, size_); }

 private:
  __attribute__((annotate("codegen"))) size_t size_;
  __attribute__((annotate("codegen:[Object*]")))
  std::vector<std::shared_ptr<Object>>
      elements_;

  friend class Client;
  friend class TupleBaseBuilder;
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif

}  // namespace vineyard

#endif  // MODULES_BASIC_DS_TUPLE_MOD_H_

namespace vineyard {


class TupleBaseBuilder: public ObjectBuilder {
  public:
    

    explicit TupleBaseBuilder(Client &client) {}

    explicit TupleBaseBuilder(
            Tuple const &__value) {
        this->set_size_(__value.size_);
        for (auto const &__elements__item: __value.elements_) {
            this->add_elements_(__elements__item);
        }
    }

    explicit TupleBaseBuilder(
            std::shared_ptr<Tuple> const & __value):
        TupleBaseBuilder(*__value) {
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<Tuple>();

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<Tuple>());
        if (std::is_base_of<GlobalObject, Tuple>::value) {
            __value->meta_.SetGlobal(true);
        }

        __value->size_ = size_;
        __value->meta_.AddKeyValue("size_", __value->size_);

        // using __elements__value_type = typename std::vector<std::shared_ptr<Object>>::value_type::element_type;
        using __elements__value_type = typename decltype(__value->elements_)::value_type::element_type;

        size_t __elements__idx = 0;
        for (auto &__elements__value: elements_) {
            auto __value_elements_ = std::dynamic_pointer_cast<__elements__value_type>(
                __elements__value->_Seal(client));
            __value->elements_.emplace_back(__value_elements_);
            __value->meta_.AddMember("__elements_-" + std::to_string(__elements__idx),
                                     __value_elements_);
            __value_nbytes += __value_elements_->nbytes();
            __elements__idx += 1;
        }
        __value->meta_.AddKeyValue("__elements_-size", __value->elements_.size());

        __value->meta_.SetNBytes(__value_nbytes);

        VINEYARD_CHECK_OK(client.CreateMetaData(__value->meta_, __value->id_));

        // mark the builder as sealed
        this->set_sealed(true);

        
        return std::static_pointer_cast<Object>(__value);
    }

    Status Build(Client &client) override {
        return Status::OK();
    }

  protected:
    size_t size_;
    std::vector<std::shared_ptr<ObjectBase>> elements_;

    void set_size_(size_t const &size__) {
        this->size_ = size__;
    }

    void set_elements_(std::vector<std::shared_ptr<ObjectBase>> const &elements__) {
        this->elements_ = elements__;
    }
    void set_elements_(size_t const idx, std::shared_ptr<ObjectBase> const &elements__) {
        if (idx >= this->elements_.size()) {
            this->elements_.resize(idx + 1);
        }
        this->elements_[idx] = elements__;
    }
    void add_elements_(std::shared_ptr<ObjectBase> const &elements__) {
        this->elements_.emplace_back(elements__);
    }
};


}  // namespace vineyard


#endif // DS_TUPLE_VINEYARD_H
