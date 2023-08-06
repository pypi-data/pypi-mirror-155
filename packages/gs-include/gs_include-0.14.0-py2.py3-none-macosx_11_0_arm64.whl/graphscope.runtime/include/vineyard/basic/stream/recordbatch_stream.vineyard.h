#ifndef STREAM_RECORDBATCH_STREAM_VINEYARD_H
#define STREAM_RECORDBATCH_STREAM_VINEYARD_H

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

#ifndef MODULES_BASIC_STREAM_RECORDBATCH_STREAM_MOD_H_
#define MODULES_BASIC_STREAM_RECORDBATCH_STREAM_MOD_H_

#include <memory>
#include <string>
#include <utility>
#include <vector>

#include "arrow/util/config.h"
#include "arrow/util/key_value_metadata.h"

#include "basic/ds/arrow.vineyard.h"
#include "basic/ds/dataframe.vineyard.h"
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

class __attribute__((annotate("no-vineyard"))) RecordBatchStreamWriter {
 public:
  const size_t MaximumChunkSize() const { return -1; }

  Status Push(std::shared_ptr<Object> const& chunk);

  Status Push(ObjectMeta const& chunk);

  Status Push(ObjectID const& chunk);

  Status Abort();

  Status Finish();

  Status WriteTable(std::shared_ptr<arrow::Table> table);

  Status WriteBatch(std::shared_ptr<arrow::RecordBatch> batch);

  Status WriteDataframe(std::shared_ptr<DataFrame> df);

  RecordBatchStreamWriter(Client& client, ObjectID const& id,
                          ObjectMeta const& meta)
      : client_(client), id_(id), meta_(meta), stoped_(false) {}

 private:
  Client& client_;
  ObjectID id_;
  ObjectMeta meta_;
  bool stoped_;  // an optimization: avoid repeated idempotent requests.

  friend class Client;
};

class __attribute__((annotate("no-vineyard"))) RecordBatchStreamReader {
 public:
  Status GetNext(std::shared_ptr<Object>& chunk);

  Status ReadRecordBatches(
      std::vector<std::shared_ptr<arrow::RecordBatch>>& batches);

  Status ReadTable(std::shared_ptr<arrow::Table>& table);

  Status ReadBatch(std::shared_ptr<arrow::RecordBatch>& batch);

  Status GetHeaderLine(bool& header_row, std::string& header_line);

  RecordBatchStreamReader(
      Client& client, ObjectID const& id, ObjectMeta const& meta,
      std::unordered_map<std::string, std::string> const& params)
      : client_(client),
        id_(id),
        meta_(meta),
        params_(params),
        batch_(nullptr),
        cursor_(0){};

 private:
  Client& client_;
  ObjectID id_;
  ObjectMeta meta_;
  std::unordered_map<std::string, std::string> params_;
  std::vector<std::shared_ptr<arrow::RecordBatch>> batches_;
  std::shared_ptr<arrow::RecordBatch> batch_;
  int64_t cursor_;

  friend class Client;
};

class RecordBatchStream : public Registered<RecordBatchStream> {
 
  public:
    static std::unique_ptr<Object> Create() __attribute__((used)) {
        return std::static_pointer_cast<Object>(
            std::unique_ptr<RecordBatchStream>{
                new RecordBatchStream()});
    }


  public:
    void Construct(const ObjectMeta& meta) override {
        std::string __type_name = type_name<RecordBatchStream>();
        VINEYARD_ASSERT(
            meta.GetTypeName() == __type_name,
            "Expect typename '" + __type_name + "', but got '" + meta.GetTypeName() + "'");
        this->meta_ = meta;
        this->id_ = meta.GetId();

        meta.GetKeyValue("params_", this->params_);

        
    }

 private:
public:
  Status OpenReader(Client& client,
                    std::unique_ptr<RecordBatchStreamReader>& reader);

  Status OpenWriter(Client& client,
                    std::unique_ptr<RecordBatchStreamWriter>& writer);

  std::unordered_map<std::string, std::string> GetParams() { return params_; }

 private:
  __attribute__((annotate("codegen")))
  std::unordered_map<std::string, std::string>
      params_;

  friend class Client;
  friend class RecordBatchStreamBaseBuilder;
};

#ifdef __GNUC__
#pragma GCC diagnostic pop
#endif

}  // namespace vineyard

#endif  // MODULES_BASIC_STREAM_RECORDBATCH_STREAM_MOD_H_

namespace vineyard {


class RecordBatchStreamBaseBuilder: public ObjectBuilder {
  public:
    

    explicit RecordBatchStreamBaseBuilder(Client &client) {}

    explicit RecordBatchStreamBaseBuilder(
            RecordBatchStream const &__value) {
        this->set_params_(__value.params_);
    }

    explicit RecordBatchStreamBaseBuilder(
            std::shared_ptr<RecordBatchStream> const & __value):
        RecordBatchStreamBaseBuilder(*__value) {
    }

    std::shared_ptr<Object> _Seal(Client &client) override {
        // ensure the builder hasn't been sealed yet.
        ENSURE_NOT_SEALED(this);

        VINEYARD_CHECK_OK(this->Build(client));
        auto __value = std::make_shared<RecordBatchStream>();

        size_t __value_nbytes = 0;

        __value->meta_.SetTypeName(type_name<RecordBatchStream>());
        if (std::is_base_of<GlobalObject, RecordBatchStream>::value) {
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


#endif // STREAM_RECORDBATCH_STREAM_VINEYARD_H
