// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import ReactDOM from "react-dom";
import { InvenioRequestsApp } from "./InvenioRequestsApp";
import {
  TimelineAcceptEvent,
  TimelineCancelEvent,
  TimelineDeclineEvent,
  TimelineExpireEvent,
  TimelineUnknownEvent,
} from "./timelineEvents";
import {
  SubmitStatus,
  DeleteStatus,
  AcceptStatus,
  DeclineStatus,
  CancelStatus,
  ExpireStatus,
} from "./request";
import { LabelTypeSubmission, LabelTypeInvitation } from "./request";
import {
  RequestAcceptButton,
  RequestCancelButton,
  RequestDeclineButton,
  RequestModalCancelButton,
} from "./components/Buttons";
import { i18next } from "@translations/invenio_requests/i18next";

const requestDetailsDiv = document.getElementById("request-detail");
const request = JSON.parse(requestDetailsDiv.dataset.record);
const defaultQueryParams = JSON.parse(
  requestDetailsDiv.dataset.defaultQueryConfig
);
const userAvatar = JSON.parse(
  requestDetailsDiv.dataset.userAvatar
);

const overriddenComponents = {
  "TimelineEvent.layout.unknown": TimelineUnknownEvent,
  "TimelineEvent.layout.declined": TimelineDeclineEvent,
  "TimelineEvent.layout.accepted": TimelineAcceptEvent,
  "TimelineEvent.layout.expired": TimelineExpireEvent,
  "TimelineEvent.layout.cancelled": TimelineCancelEvent,
  "RequestStatus.layout.submitted": SubmitStatus,
  "RequestStatus.layout.deleted": DeleteStatus,
  "RequestStatus.layout.accepted": AcceptStatus,
  "RequestStatus.layout.declined": DeclineStatus,
  "RequestStatus.layout.cancelled": CancelStatus,
  "RequestStatus.layout.expired": ExpireStatus,
  "RequestTypeLabel.layout.community-submission": LabelTypeSubmission,
  "RequestTypeLabel.layout.community-invitation": LabelTypeInvitation,
  "RequestAction.button.cancel": RequestCancelButton,
  "RequestAction.button.accept": RequestAcceptButton,
  "RequestAction.button.decline": RequestDeclineButton,
  "RequestActionModal.button.cancel": RequestModalCancelButton,
  "RequestActionModal.button.accept": RequestAcceptButton,
  "RequestActionModal.button.decline": RequestDeclineButton,
  "RequestActionModal.title.cancel": () => i18next.t("Cancel request"),
  "RequestActionModal.title.accept": () => i18next.t("Accept request"),
  "RequestActionModal.title.decline": () => i18next.t("Decline request"),
};

ReactDOM.render(
  <InvenioRequestsApp
    request={request}
    defaultQueryParams={defaultQueryParams}
    overriddenCmps={overriddenComponents}
    userAvatar={userAvatar}
  />,
  requestDetailsDiv
);
