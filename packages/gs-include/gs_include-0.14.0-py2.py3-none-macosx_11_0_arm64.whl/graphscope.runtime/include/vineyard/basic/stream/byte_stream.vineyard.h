#ifndef STREAM_BYTE_STREAM_VINEYARD_H
#define STREAM_BYTE_STREAM_VINEYARD_H

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

#ifndef MODULES_BASIC_STREAM_BYTE_STREAM_MOD_H_
#define MODULES_BASIC_STREAM_BYTE_STREAM_MOD_H_

#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "arrow/builder.h"
#include "arrow/status.h"

#include "basic/ds/arrow_utils.h"
#include "client/client.h"
#include "client/ds/blob.h"
#include "client/ds/i_object.h"
#include "common/util/uuid.h"

namespace vineyard {

#ifdef __GNUC__
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wattributes"
#endif

class Client;

class __attribute__((annotate("no-vineyard"))) ByteStreamWriter {
 public:
  const size_t MaximumChunkSize() const { return -1; }

  Status GetNext(size_t const size,
                 std::unique_ptr<arrow::MutableBuffer>& buffer);

  Status Abort();

  Status Finish();

  Status WriteBytes(const char* ptr, size_t len);

  Status WriteLine(const std::string& line);

  void SetBufferSizeLimit(size_t limit) { buffer_size_limit_ = limit; }

  ByteStreamWriter(Client& client, ObjectID const& id, ObjectMeta const& meta)
      : client_(client), id_(id), meta_(meta), stoped_(false) {}

 private:
  Status flushBuffer();

  Client& client_;
  ObjectID id_;
  ObjectMeta meta_;
  bool stoped_;  // an optimization: avoid repeated idempotent requests.

  arrow::BufferBuilder builder_;
  size_t buffer_size_limit_ = 1024 * 1024 * 256;  // 256Mi

  friend class Client;
};

class __attribute__((annotate("no-vineyard"))) ByteStreamReader {
 public:
  Status GetNext(std::unique_ptr<arrow::Buffer>& buffer);

  Status ReadLine(std::string& line);

  ByteStreamReader(Client& client, ObjectID const& id, ObjectMeta const& meta)
      : client_(client), id_(id), meta_(meta){};

 private:
  Client& client_;
  ObjectID id_;
  ObjectMeta meta_;
  std::stringstream ss_;

  friend class Client;
};

class ByteStreamBaseBuilder;

/**
 * @brief The basic stream with each chunk representing a segment of bytes
 *
 */
class ByteStream : public Registered<ByteStream> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<ByteStream>{
                new ByteStream()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<ByteStream>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        meta.GetKeyValue("params_", this->params_);

        
    }

 private:
public:
  /**
   * @brief Open a reader to consume data from the byte stream
   *
   * @param client The client connected to the vineyard server
   * @param The unique pointer to the reader
   */
  Status OpenReader(Client& client, std::unique_ptr<ByteStreamReader>& reader);

  /**
   * @brief Open a writer to produce data to the byte stream
   *
   * @param client The client connected to the vineyard server
   * @param The unique pointer to the writer
   */
  Status OpenWriter(Client& client, std::unique_ptr<ByteStreamWriter>& writer);

  std::unordered_map<std::string, std::string> GetParams() { return params_; }

 private:
  __attribute__((annotate("codegen")))
  std::unordered_map<std::string, std::string>
      params_;

  friend class Client;
  friend class ByteStreamBaseBuilder;
  friend class ByteStreamBuilder;
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif

}  // namespace vineyard

#endif  // MODULES_BASIC_STREAM_BYTE_STREAM_MOD_H_

namespace vineyard {


class ByteStreamBaseBuilder: public ObjectBuilder {
  public:
    

    explicit ByteStreamBaseBuilder(Client &client) {}

    explicit ByteStreamBaseBuilder(
            ByteStream const &__value) {
        this->set_params_(__value.params_);
    }

    explicit ByteStreamBaseBuilder(
            std::shared_ptr<ByteStream> const & __value):
        ByteStreamBaseBuilder(*__value) {
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<ByteStream>();

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<ByteStream>());
        if (std::is_base_of<GlobalObject, ByteStream>::value) {
            __value->meta_.SetGlobal(true);
        }

        __value->params_ = params_;
        __value->meta_.AddKeyValue("params_", __value->params_);

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
    std::unordered_map<std::string, std::string> params_;

    void set_params_(std::unordered_map<std::string, std::string> const &params__) {
        this->params_ = params__;
    }
};


}  // namespace vineyard


#endif // STREAM_BYTE_STREAM_VINEYARD_H
