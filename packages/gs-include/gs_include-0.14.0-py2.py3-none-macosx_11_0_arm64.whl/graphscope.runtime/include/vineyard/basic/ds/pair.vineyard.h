#ifndef DS_PAIR_VINEYARD_H
#define DS_PAIR_VINEYARD_H

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

#ifndef MODULES_BASIC_DS_PAIR_MOD_H_
#define MODULES_BASIC_DS_PAIR_MOD_H_

#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "client/client.h"
#include "client/ds/blob.h"
#include "client/ds/i_object.h"
#include "common/util/uuid.h"

namespace vineyard {

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

class PairBaseBuilder;

class Pair : public Registered<Pair> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<Pair>{
                new Pair()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<Pair>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        this->first_ = std::dynamic_pointer_cast<Object>(meta.GetMember("first_"));
        this->second_ = std::dynamic_pointer_cast<Object>(meta.GetMember("second_"));

        
    }

 private:
public:
  /**
   * @brief Get the first element of the pair.
   *
   * @return The shared pointer to the first object.
   */
  std::shared_ptr<Object> const First() const { return first_; }

  /**
   * @brief Get the second element of the pair.
   *
   * @return The shared pointer to the second object.
   */
  std::shared_ptr<Object> const Second() const { return second_; }

  /**
   * @brief The iterator for the pair object to iterate from the first to the
   * last element.
   *
   */
  class iterator
      : public std::iterator<
            std::bidirectional_iterator_tag, std::shared_ptr<Object>, size_t,
            const std::shared_ptr<Object>*, std::shared_ptr<Object>> {
    Pair const* pair_;
    size_t index_;

   public:
    explicit iterator(Pair const* pair, size_t index = 0)
        : pair_(pair), index_(index) {}
    iterator& operator++() {
      index_ += 1;
      return *this;
    }
    bool operator==(iterator other) const { return index_ == other.index_; }
    bool operator!=(iterator other) const { return index_ != other.index_; }
    reference operator*() const {
      return index_ == 0 ? pair_->First() : pair_->Second();
    }
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
  const iterator end() const { return iterator(this, 2); }

 private:
  __attribute__((annotate("codegen:Object*"))) std::shared_ptr<Object> first_,
      second_;

  friend class Client;
  friend class PairBaseBuilder;
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif

}  // namespace vineyard

#endif  // MODULES_BASIC_DS_PAIR_MOD_H_

namespace vineyard {


class PairBaseBuilder: public ObjectBuilder {
  public:
    

    explicit PairBaseBuilder(Client &client) {}

    explicit PairBaseBuilder(
            Pair const &__value) {
        this->set_first_(__value.first_);
        this->set_second_(__value.second_);
    }

    explicit PairBaseBuilder(
            std::shared_ptr<Pair> const & __value):
        PairBaseBuilder(*__value) {
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<Pair>();

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<Pair>());
        if (std::is_base_of<GlobalObject, Pair>::value) {
            __value->meta_.SetGlobal(true);
        }

        // using __first__value_type = typename std::shared_ptr<Object>::element_type;
        using __first__value_type = typename decltype(__value->first_)::element_type;
        auto __value_first_ = std::dynamic_pointer_cast<__first__value_type>(
            first_->_Seal(client));
        __value->first_ = __value_first_;
        __value->meta_.AddMember("first_", __value->first_);
        __value_nbytes += __value_first_->nbytes();

        // using __second__value_type = typename std::shared_ptr<Object>::element_type;
        using __second__value_type = typename decltype(__value->second_)::element_type;
        auto __value_second_ = std::dynamic_pointer_cast<__second__value_type>(
            second_->_Seal(client));
        __value->second_ = __value_second_;
        __value->meta_.AddMember("second_", __value->second_);
        __value_nbytes += __value_second_->nbytes();

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
    std::shared_ptr<ObjectBase> first_;
    std::shared_ptr<ObjectBase> second_;

    void set_first_(std::shared_ptr<ObjectBase> const & first__) {
        this->first_ = first__;
    }

    void set_second_(std::shared_ptr<ObjectBase> const & second__) {
        this->second_ = second__;
    }
};


}  // namespace vineyard


#endif // DS_PAIR_VINEYARD_H
